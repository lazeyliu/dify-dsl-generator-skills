#!/usr/bin/env python3

from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path


SPECIAL_SELECTOR_ROOTS = {"sys", "env", "conversation"}


def load_yaml_via_ruby(path: Path) -> dict:
    ruby_code = """
require "yaml"
require "json"

path = ARGV[0]
data = YAML.load_file(path)
puts JSON.generate(data)
"""
    result = subprocess.run(
        ["ruby", "-e", ruby_code, str(path)],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "Ruby YAML 解析失败")
    return json.loads(result.stdout)


def get_node_type(node: dict) -> str:
    if not isinstance(node, dict):
        return ""
    data = node.get("data") or {}
    node_type = data.get("type") or node.get("type")
    return node_type if isinstance(node_type, str) else ""


def add_issue(issues: list[dict], severity: str, code: str, path: str, message: str) -> None:
    issues.append(
        {
            "severity": severity,
            "code": code,
            "path": path,
            "message": message,
        }
    )


def validate_selector(
    issues: list[dict],
    selector: object,
    path: str,
    node_ids: set[str],
) -> None:
    if not isinstance(selector, list) or len(selector) < 2:
        add_issue(issues, "error", "selector_shape_invalid", path, "选择器必须是长度至少为 2 的数组")
        return

    root = selector[0]
    if not isinstance(root, str):
        add_issue(issues, "error", "selector_root_invalid", path, "选择器首项必须是字符串")
        return

    if root in SPECIAL_SELECTOR_ROOTS or root in node_ids:
        return

    add_issue(issues, "error", "selector_target_missing", path, f"选择器引用了不存在的节点或系统根: {root}")


def validate_end_outputs(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    outputs = ((node.get("data") or {}).get("outputs")) or []
    for index, output in enumerate(outputs):
        selector = output.get("value_selector")
        if selector is not None:
            validate_selector(
                issues,
                selector,
                f"nodes[{node['id']}].data.outputs[{index}].value_selector",
                node_ids,
            )


def validate_if_else(issues: list[dict], node: dict, outgoing_handles: set[str], node_ids: set[str]) -> None:
    data = node.get("data") or {}
    cases = data.get("cases")
    if not isinstance(cases, list) or not cases:
        add_issue(issues, "error", "if_else_cases_missing", f"nodes[{node['id']}].data.cases", "if-else 缺少 cases")
        return

    allowed_handles = {"false"}
    for case_index, case in enumerate(cases):
        case_id = case.get("case_id")
        if not case_id:
            add_issue(
                issues,
                "error",
                "if_else_case_id_missing",
                f"nodes[{node['id']}].data.cases[{case_index}].case_id",
                "if-else case 缺少 case_id",
            )
            continue
        allowed_handles.add(str(case_id))
        for cond_index, condition in enumerate(case.get("conditions") or []):
            selector = condition.get("variable_selector")
            if selector is not None:
                validate_selector(
                    issues,
                    selector,
                    f"nodes[{node['id']}].data.cases[{case_index}].conditions[{cond_index}].variable_selector",
                    node_ids,
                )

    unexpected_handles = sorted(handle for handle in outgoing_handles if handle and handle not in allowed_handles)
    for handle in unexpected_handles:
        add_issue(
            issues,
            "error",
            "if_else_handle_unexpected",
            f"edges[source={node['id']}].sourceHandle",
            f"if-else 存在未在 cases 中声明的分支句柄: {handle}",
        )

    if "false" not in outgoing_handles:
        add_issue(
            issues,
            "error",
            "if_else_false_missing",
            f"edges[source={node['id']}]",
            "if-else 未显式提供 false/default 分支",
        )


def validate_question_classifier(issues: list[dict], node: dict, outgoing_handles: set[str], node_ids: set[str]) -> None:
    data = node.get("data") or {}
    query_selector = data.get("query_variable_selector")
    if query_selector is None:
        add_issue(
            issues,
            "error",
            "question_classifier_query_missing",
            f"nodes[{node['id']}].data.query_variable_selector",
            "question-classifier 缺少 query_variable_selector",
        )
    else:
        validate_selector(issues, query_selector, f"nodes[{node['id']}].data.query_variable_selector", node_ids)

    classes = data.get("classes")
    if not isinstance(classes, list) or not classes:
        add_issue(
            issues,
            "error",
            "question_classifier_classes_missing",
            f"nodes[{node['id']}].data.classes",
            "question-classifier 缺少 classes",
        )
        return

    class_id_list: list[str] = []
    class_ids = set()
    for class_index, class_item in enumerate(classes):
        class_id = class_item.get("id")
        if not class_id:
            add_issue(
                issues,
                "error",
                "question_classifier_class_id_missing",
                f"nodes[{node['id']}].data.classes[{class_index}].id",
                "question-classifier 类别缺少 id",
            )
            continue
        class_id = str(class_id)
        class_id_list.append(class_id)
        class_ids.add(class_id)

        class_name = class_item.get("name")
        if not isinstance(class_name, str) or not class_name.strip():
            add_issue(
                issues,
                "error",
                "question_classifier_class_name_missing",
                f"nodes[{node['id']}].data.classes[{class_index}].name",
                "question-classifier 类别缺少 name",
            )

    for class_id, count in Counter(class_id_list).items():
        if count > 1:
            add_issue(
                issues,
                "error",
                "question_classifier_class_id_duplicate",
                f"nodes[{node['id']}].data.classes",
                f"question-classifier 存在重复 class id: {class_id}",
            )

    unexpected_handles = sorted(handle for handle in outgoing_handles if handle and handle not in class_ids)
    for handle in unexpected_handles:
        add_issue(
            issues,
            "error",
            "question_classifier_handle_unexpected",
            f"edges[source={node['id']}].sourceHandle",
            f"question-classifier 存在未在 classes 中声明的句柄: {handle}",
        )

    missing_handles = sorted(class_id for class_id in class_ids if class_id not in outgoing_handles)
    for handle in missing_handles:
        add_issue(
            issues,
            "error",
            "question_classifier_handle_missing",
            f"edges[source={node['id']}]",
            f"question-classifier 缺少类别句柄对应出口: {handle}",
        )


def validate_parameter_extractor(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    data = node.get("data") or {}
    query_selector = data.get("query")
    if query_selector is None:
        add_issue(
            issues,
            "error",
            "parameter_extractor_query_missing",
            f"nodes[{node['id']}].data.query",
            "parameter-extractor 缺少 query",
        )
    else:
        validate_selector(issues, query_selector, f"nodes[{node['id']}].data.query", node_ids)

    if not data.get("reasoning_mode"):
        add_issue(
            issues,
            "error",
            "parameter_extractor_reasoning_mode_missing",
            f"nodes[{node['id']}].data.reasoning_mode",
            "parameter-extractor 缺少 reasoning_mode",
        )

    parameters = data.get("parameters")
    if not isinstance(parameters, list) or not parameters:
        add_issue(
            issues,
            "error",
            "parameter_extractor_parameters_missing",
            f"nodes[{node['id']}].data.parameters",
            "parameter-extractor 缺少 parameters",
        )


def validate_knowledge_retrieval(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    data = node.get("data") or {}
    dataset_ids = data.get("dataset_ids")
    if not isinstance(dataset_ids, list) or not dataset_ids:
        add_issue(
            issues,
            "error",
            "knowledge_retrieval_dataset_ids_missing",
            f"nodes[{node['id']}].data.dataset_ids",
            "knowledge-retrieval 的 dataset_ids 不能为空",
        )

    query_selector = data.get("query_variable_selector")
    if query_selector is None:
        add_issue(
            issues,
            "error",
            "knowledge_retrieval_query_missing",
            f"nodes[{node['id']}].data.query_variable_selector",
            "knowledge-retrieval 缺少 query_variable_selector",
        )
    else:
        validate_selector(issues, query_selector, f"nodes[{node['id']}].data.query_variable_selector", node_ids)

    retrieval_mode = data.get("retrieval_mode")
    if retrieval_mode not in {"multiple", "single"}:
        add_issue(
            issues,
            "error",
            "knowledge_retrieval_mode_invalid",
            f"nodes[{node['id']}].data.retrieval_mode",
            "knowledge-retrieval 的 retrieval_mode 只能是 single 或 multiple",
        )
    if retrieval_mode == "multiple" and not isinstance(data.get("multiple_retrieval_config"), dict):
        add_issue(
            issues,
            "error",
            "knowledge_retrieval_multiple_config_missing",
            f"nodes[{node['id']}].data.multiple_retrieval_config",
            "retrieval_mode=multiple 时必须提供 multiple_retrieval_config",
        )
    elif retrieval_mode == "multiple":
        config = data.get("multiple_retrieval_config") or {}
        top_k = config.get("top_k")
        if not isinstance(top_k, int) or top_k < 1:
            add_issue(
                issues,
                "error",
                "knowledge_retrieval_topk_invalid",
                f"nodes[{node['id']}].data.multiple_retrieval_config.top_k",
                "knowledge-retrieval 的 top_k 必须是大于等于 1 的整数",
            )
        if config.get("score_threshold_enabled") and not isinstance(config.get("score_threshold"), (int, float)):
            add_issue(
                issues,
                "error",
                "knowledge_retrieval_score_threshold_invalid",
                f"nodes[{node['id']}].data.multiple_retrieval_config.score_threshold",
                "开启 score_threshold_enabled 时必须提供数值型 score_threshold",
            )
    if retrieval_mode == "single":
        single_model = ((data.get("single_retrieval_config") or {}).get("model"))
        if not isinstance(single_model, dict):
            add_issue(
                issues,
                "error",
                "knowledge_retrieval_single_model_missing",
                f"nodes[{node['id']}].data.single_retrieval_config.model",
                "retrieval_mode=single 时必须提供 single_retrieval_config.model",
            )


def validate_list_operator(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    data = node.get("data") or {}
    variable = data.get("variable")
    if variable is None:
        add_issue(issues, "error", "list_operator_variable_missing", f"nodes[{node['id']}].data.variable", "list-operator 缺少 variable")
    else:
        validate_selector(issues, variable, f"nodes[{node['id']}].data.variable", node_ids)

    for key in ("filter_by", "order_by", "limit"):
        if key not in data:
            add_issue(
                issues,
                "error",
                f"list_operator_{key}_missing",
                f"nodes[{node['id']}].data.{key}",
                f"list-operator 缺少 {key}",
            )

    filter_by = data.get("filter_by") or {}
    if isinstance(filter_by, dict) and filter_by.get("enabled") and not (filter_by.get("conditions") or []):
        add_issue(
            issues,
            "error",
            "list_operator_filter_conditions_missing",
            f"nodes[{node['id']}].data.filter_by.conditions",
            "list-operator 开启 filter_by 时必须提供 conditions",
        )

    order_by = data.get("order_by") or {}
    if isinstance(order_by, dict) and order_by.get("enabled"):
        if order_by.get("value") not in {"asc", "desc"}:
            add_issue(
                issues,
                "error",
                "list_operator_order_invalid",
                f"nodes[{node['id']}].data.order_by.value",
                "list-operator 开启 order_by 时 value 只能是 asc 或 desc",
            )

    limit = data.get("limit") or {}
    if isinstance(limit, dict) and limit.get("enabled"):
        size = limit.get("size")
        if not isinstance(size, int) or size < 1:
            add_issue(
                issues,
                "error",
                "list_operator_limit_invalid",
                f"nodes[{node['id']}].data.limit.size",
                "list-operator 开启 limit 时 size 必须是大于等于 1 的整数",
            )


def validate_iteration(issues: list[dict], node: dict, node_types: dict[str, str], node_ids: set[str]) -> None:
    data = node.get("data") or {}
    for field in ("iterator_selector", "output_selector", "start_node_id"):
        if field not in data:
            add_issue(
                issues,
                "error",
                f"iteration_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"iteration 缺少 {field}",
            )

    if "iterator_selector" in data:
        validate_selector(issues, data["iterator_selector"], f"nodes[{node['id']}].data.iterator_selector", node_ids)
    if "output_selector" in data:
        validate_selector(issues, data["output_selector"], f"nodes[{node['id']}].data.output_selector", node_ids)

    start_node_id = data.get("start_node_id")
    if start_node_id and node_types.get(start_node_id) != "iteration-start":
        add_issue(
            issues,
            "error",
            "iteration_start_node_invalid",
            f"nodes[{node['id']}].data.start_node_id",
            f"iteration 的 start_node_id 未指向 iteration-start 节点: {start_node_id}",
        )


def validate_loop(issues: list[dict], node: dict, node_types: dict[str, str], node_ids: set[str]) -> None:
    data = node.get("data") or {}
    for field in ("loop_count", "break_conditions", "logical_operator", "start_node_id"):
        if field not in data:
            add_issue(
                issues,
                "error",
                f"loop_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"loop 缺少 {field}",
            )

    start_node_id = data.get("start_node_id")
    if start_node_id and node_types.get(start_node_id) != "loop-start":
        add_issue(
            issues,
            "error",
            "loop_start_node_invalid",
            f"nodes[{node['id']}].data.start_node_id",
            f"loop 的 start_node_id 未指向 loop-start 节点: {start_node_id}",
        )

    for cond_index, condition in enumerate(data.get("break_conditions") or []):
        selector = condition.get("variable_selector")
        if selector is not None:
            validate_selector(
                issues,
                selector,
                f"nodes[{node['id']}].data.break_conditions[{cond_index}].variable_selector",
                node_ids,
            )


def validate_variable_aggregator(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    data = node.get("data") or {}
    if not data.get("output_type"):
        add_issue(
            issues,
            "error",
            "variable_aggregator_output_type_missing",
            f"nodes[{node['id']}].data.output_type",
            "variable-aggregator 缺少 output_type",
        )
    variables = data.get("variables")
    if not isinstance(variables, list) or not variables:
        add_issue(
            issues,
            "error",
            "variable_aggregator_variables_missing",
            f"nodes[{node['id']}].data.variables",
            "variable-aggregator 缺少 variables",
        )
        return

    for index, selector in enumerate(variables):
        validate_selector(issues, selector, f"nodes[{node['id']}].data.variables[{index}]", node_ids)


def validate_assigner(issues: list[dict], node: dict, node_ids: set[str]) -> None:
    data = node.get("data") or {}
    if data.get("version") != "2":
        add_issue(
            issues,
            "warning",
            "assigner_version_not_explicit",
            f"nodes[{node['id']}].data.version",
            "assigner 建议显式使用 version: \"2\"",
        )

    items = data.get("items")
    if not isinstance(items, list) or not items:
        add_issue(
            issues,
            "error",
            "assigner_items_missing",
            f"nodes[{node['id']}].data.items",
            "assigner 缺少 items",
        )
        return

    for index, item in enumerate(items):
        selector = item.get("variable_selector")
        if selector is None:
            add_issue(
                issues,
                "error",
                "assigner_target_missing",
                f"nodes[{node['id']}].data.items[{index}].variable_selector",
                "assigner item 缺少 variable_selector",
            )
        else:
            validate_selector(issues, selector, f"nodes[{node['id']}].data.items[{index}].variable_selector", node_ids)
        if item.get("input_type") == "variable":
            value = item.get("value")
            validate_selector(issues, value, f"nodes[{node['id']}].data.items[{index}].value", node_ids)


def validate_human_input(issues: list[dict], node: dict) -> None:
    data = node.get("data") or {}
    delivery_methods = data.get("delivery_methods")
    if not isinstance(delivery_methods, list) or not delivery_methods:
        add_issue(
            issues,
            "error",
            "human_input_delivery_missing",
            f"nodes[{node['id']}].data.delivery_methods",
            "human-input 缺少 delivery_methods",
        )
    user_actions = data.get("user_actions")
    if not isinstance(user_actions, list) or not user_actions:
        add_issue(
            issues,
            "error",
            "human_input_actions_missing",
            f"nodes[{node['id']}].data.user_actions",
            "human-input 缺少 user_actions",
        )
    else:
        action_ids = [action.get("id") for action in user_actions if isinstance(action, dict)]
        duplicates = [action_id for action_id, count in Counter(action_ids).items() if action_id and count > 1]
        for action_id in duplicates:
            add_issue(
                issues,
                "error",
                "human_input_action_id_duplicate",
                f"nodes[{node['id']}].data.user_actions",
                f"human-input 的 user_actions 存在重复 id: {action_id}",
            )
        if "__timeout" not in action_ids:
            add_issue(
                issues,
                "warning",
                "human_input_timeout_path_missing",
                f"nodes[{node['id']}].data.user_actions",
                "human-input 未显式声明 __timeout 恢复路径",
            )

    inputs = data.get("inputs")
    if isinstance(inputs, list):
        output_names = [item.get("output_variable_name") for item in inputs if isinstance(item, dict)]
        duplicates = [name for name, count in Counter(output_names).items() if name and count > 1]
        for output_name in duplicates:
            add_issue(
                issues,
                "error",
                "human_input_output_name_duplicate",
                f"nodes[{node['id']}].data.inputs",
                f"human-input 的 outputs 存在重复 output_variable_name: {output_name}",
            )
    for field in ("timeout", "timeout_unit", "form_content", "inputs"):
        if field not in data:
            add_issue(
                issues,
                "warning",
                f"human_input_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"human-input 建议显式声明 {field}",
            )


def validate_trigger_webhook(issues: list[dict], node: dict) -> None:
    data = node.get("data") or {}
    for field in ("method", "content_type", "headers", "params", "body"):
        if field not in data:
            add_issue(
                issues,
                "warning",
                f"trigger_webhook_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"trigger-webhook 建议显式声明 {field}",
            )

    body = data.get("body")
    if body is not None and not isinstance(body, list):
        add_issue(
            issues,
            "error",
            "trigger_webhook_body_invalid_type",
            f"nodes[{node['id']}].data.body",
            "trigger-webhook 的 body 必须是参数数组",
        )


def validate_trigger_schedule(issues: list[dict], node: dict) -> None:
    data = node.get("data") or {}
    for field in ("mode", "timezone"):
        if field not in data:
            add_issue(
                issues,
                "warning",
                f"trigger_schedule_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"trigger-schedule 建议显式声明 {field}",
            )

    mode = data.get("mode")
    if mode == "cron" and not data.get("cron_expression"):
        add_issue(
            issues,
            "error",
            "trigger_schedule_cron_missing",
            f"nodes[{node['id']}].data.cron_expression",
            "trigger-schedule 在 mode=cron 时必须提供 cron_expression",
        )
    if mode == "visual":
        if not data.get("frequency"):
            add_issue(
                issues,
                "error",
                "trigger_schedule_frequency_missing",
                f"nodes[{node['id']}].data.frequency",
                "trigger-schedule 在 mode=visual 时必须提供 frequency",
            )
        if not isinstance(data.get("visual_config"), dict):
            add_issue(
                issues,
                "error",
                "trigger_schedule_visual_config_missing",
                f"nodes[{node['id']}].data.visual_config",
                "trigger-schedule 在 mode=visual 时必须提供 visual_config",
            )


def validate_trigger_plugin(issues: list[dict], node: dict) -> None:
    data = node.get("data") or {}
    for field in (
        "plugin_id",
        "provider_id",
        "event_name",
        "subscription_id",
        "plugin_unique_identifier",
        "event_parameters",
    ):
        if field not in data:
            add_issue(
                issues,
                "error",
                f"trigger_plugin_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"trigger-plugin 缺少 {field}",
            )

    if "event_parameters" in data and not isinstance(data.get("event_parameters"), dict):
        add_issue(
            issues,
            "error",
            "trigger_plugin_event_parameters_invalid",
            f"nodes[{node['id']}].data.event_parameters",
            "trigger-plugin 的 event_parameters 必须是对象",
        )


def validate_agent(issues: list[dict], node: dict) -> None:
    data = node.get("data") or {}
    for field in ("agent_strategy_provider_name", "agent_strategy_name", "agent_strategy_label", "agent_parameters"):
        if field not in data:
            add_issue(
                issues,
                "error",
                f"agent_{field}_missing",
                f"nodes[{node['id']}].data.{field}",
                f"agent 缺少 {field}",
            )

    for field in ("agent_strategy_provider_name", "agent_strategy_name", "agent_strategy_label"):
        value = data.get(field)
        if field in data and (not isinstance(value, str) or not value.strip()):
            add_issue(
                issues,
                "error",
                f"{field}_invalid",
                f"nodes[{node['id']}].data.{field}",
                f"agent 的 {field} 必须是非空字符串",
            )

    if "tool_node_version" in data and data.get("tool_node_version") != "2":
        add_issue(
            issues,
            "error",
            "agent_tool_node_version_invalid",
            f"nodes[{node['id']}].data.tool_node_version",
            "agent 的 tool_node_version 必须是 \"2\"",
        )

    if "agent_parameters" in data and not isinstance(data.get("agent_parameters"), dict):
        add_issue(
            issues,
            "error",
            "agent_parameters_invalid_type",
            f"nodes[{node['id']}].data.agent_parameters",
            "agent 的 agent_parameters 必须是对象",
        )


def lint_dsl(path: Path, data: dict) -> dict:
    issues: list[dict] = []
    kind = data.get("kind", "")
    app = data.get("app") or {}
    mode = app.get("mode", "")
    workflow = data.get("workflow") or {}
    graph = workflow.get("graph") or {}
    nodes = graph.get("nodes") or []
    edges = graph.get("edges") or []

    if not nodes:
        add_issue(issues, "error", "nodes_missing", "workflow.graph.nodes", "缺少 nodes")
    if not edges:
        add_issue(issues, "warning", "edges_missing", "workflow.graph.edges", "缺少 edges")

    node_ids: list[str] = []
    node_types: dict[str, str] = {}
    type_counts: Counter[str] = Counter()
    for index, node in enumerate(nodes):
        node_id = node.get("id")
        if not node_id:
            add_issue(issues, "error", "node_id_missing", f"nodes[{index}].id", "节点缺少 id")
            continue
        node_ids.append(str(node_id))
        node_type = get_node_type(node)
        if not node_type:
            add_issue(issues, "error", "node_type_missing", f"nodes[{node_id}].data.type", "节点缺少 data.type")
            continue
        node_types[str(node_id)] = node_type
        type_counts[node_type] += 1

    duplicates = [node_id for node_id, count in Counter(node_ids).items() if count > 1]
    for node_id in duplicates:
        add_issue(issues, "error", "node_id_duplicate", f"nodes[{node_id}].id", f"节点 id 重复: {node_id}")

    node_id_set = set(node_types)
    outgoing_handles: dict[str, set[str]] = defaultdict(set)
    for edge_index, edge in enumerate(edges):
        source = edge.get("source")
        target = edge.get("target")
        if source not in node_id_set:
            add_issue(
                issues,
                "error",
                "edge_source_missing",
                f"edges[{edge_index}].source",
                f"边引用了不存在的 source 节点: {source}",
            )
        if target not in node_id_set:
            add_issue(
                issues,
                "error",
                "edge_target_missing",
                f"edges[{edge_index}].target",
                f"边引用了不存在的 target 节点: {target}",
            )
        if source:
            handle = edge.get("sourceHandle")
            if isinstance(handle, str):
                outgoing_handles[str(source)].add(handle)

    if type_counts.get("start", 0) and any(node_type.startswith("trigger-") for node_type in type_counts):
        add_issue(
            issues,
            "error",
            "mixed_start_and_trigger",
            "workflow.graph.nodes",
            "普通 start 与 trigger-* 入口不应默认并列存在",
        )

    if kind == "app" and mode == "workflow" and not type_counts.get("end", 0):
        add_issue(issues, "error", "workflow_end_missing", "workflow.graph.nodes", "workflow 缺少 end 节点")
    if kind == "app" and mode == "advanced-chat" and not type_counts.get("answer", 0):
        add_issue(issues, "error", "advanced_chat_answer_missing", "workflow.graph.nodes", "advanced-chat 缺少 answer 节点")
    if kind == "rag_pipeline" and "rag_pipeline" not in data:
        add_issue(issues, "error", "rag_pipeline_block_missing", "rag_pipeline", "kind=rag_pipeline 时必须存在 rag_pipeline 顶层块")

    for node in nodes:
        node_id = str(node.get("id"))
        node_type = node_types.get(node_id)
        if not node_type:
            continue

        if node_type == "end":
            validate_end_outputs(issues, node, node_id_set)
        elif node_type == "if-else":
            validate_if_else(issues, node, outgoing_handles.get(node_id, set()), node_id_set)
        elif node_type == "question-classifier":
            validate_question_classifier(issues, node, outgoing_handles.get(node_id, set()), node_id_set)
        elif node_type == "parameter-extractor":
            validate_parameter_extractor(issues, node, node_id_set)
        elif node_type == "knowledge-retrieval":
            validate_knowledge_retrieval(issues, node, node_id_set)
        elif node_type == "list-operator":
            validate_list_operator(issues, node, node_id_set)
        elif node_type == "iteration":
            validate_iteration(issues, node, node_types, node_id_set)
        elif node_type == "loop":
            validate_loop(issues, node, node_types, node_id_set)
        elif node_type == "variable-aggregator":
            validate_variable_aggregator(issues, node, node_id_set)
        elif node_type == "assigner":
            validate_assigner(issues, node, node_id_set)
        elif node_type == "human-input":
            validate_human_input(issues, node)
        elif node_type == "trigger-webhook":
            validate_trigger_webhook(issues, node)
        elif node_type == "trigger-schedule":
            validate_trigger_schedule(issues, node)
        elif node_type == "trigger-plugin":
            validate_trigger_plugin(issues, node)
        elif node_type == "agent":
            validate_agent(issues, node)

    error_count = sum(1 for issue in issues if issue["severity"] == "error")
    warning_count = sum(1 for issue in issues if issue["severity"] == "warning")
    return {
        "path": str(path),
        "kind": kind or "(unknown)",
        "mode": mode or "(unknown)",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "error_count": error_count,
        "warning_count": warning_count,
        "issues": issues,
    }


def render_report(report: dict) -> str:
    lines = [
        f"样本: {report['path']}",
        f"kind: {report['kind']}",
        f"mode: {report['mode']}",
        f"节点数: {report['node_count']}",
        f"边数: {report['edge_count']}",
        f"错误数: {report['error_count']}",
        f"警告数: {report['warning_count']}",
    ]
    if report["issues"]:
        lines.append("")
        lines.append("问题列表:")
        for issue in report["issues"]:
            lines.append(
                f"- [{issue['severity']}] {issue['code']} | {issue['path']} | {issue['message']}"
            )
    else:
        lines.append("")
        lines.append("问题列表:")
        lines.append("- 未发现问题。")
    return "\n".join(lines)


def main() -> int:
    if len(sys.argv) not in {2, 3}:
        print("用法: python3 scripts/lint_dsl.py <dsl-path> [--json]", file=sys.stderr)
        return 1

    path = Path(sys.argv[1]).expanduser().resolve()
    if not path.exists():
        print(f"错误: {path} 不存在", file=sys.stderr)
        return 1

    emit_json = len(sys.argv) == 3 and sys.argv[2] == "--json"
    if len(sys.argv) == 3 and not emit_json:
        print("错误: 仅支持可选参数 --json", file=sys.stderr)
        return 1

    try:
        data = load_yaml_via_ruby(path)
    except Exception as exc:
        print(f"错误: {exc}", file=sys.stderr)
        return 1

    report = lint_dsl(path, data)
    if emit_json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_report(report))
    return 1 if report["error_count"] > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
