#!/usr/bin/env ruby

require "pathname"
require "yaml"

MAX_SKILL_NAME_LENGTH = 64
MAX_DESCRIPTION_LENGTH = 1024
ALLOWED_FRONTMATTER_KEYS = %w[name description].freeze
FRONTMATTER_PATTERN = /\A---\r?\n(.*?)\r?\n---(?:\r?\n|\z)/m

def read_text(path)
  path.read
end

def find_skill_dirs(target)
  if target.file? && target.basename.to_s == "SKILL.md"
    return [target.dirname]
  end

  if (target + "SKILL.md").exist?
    return [target]
  end

  skills_root = target + "skills"
  return [] unless skills_root.directory?

  skills_root.children.select(&:directory?).select { |path| (path + "SKILL.md").exist? }.sort
end

def parse_frontmatter(skill_md_path)
  content = read_text(skill_md_path)
  match = content.match(FRONTMATTER_PATTERN)
  return nil, content, ["#{skill_md_path}: 缺少或无法识别 YAML frontmatter"] if match.nil?

  begin
    frontmatter = YAML.safe_load(match[1], permitted_classes: [], aliases: false)
  rescue Psych::Exception => e
    return nil, content, ["#{skill_md_path}: frontmatter YAML 无法解析: #{e.message.lines.first&.strip}"]
  end

  unless frontmatter.is_a?(Hash)
    return nil, content, ["#{skill_md_path}: frontmatter 必须是 YAML 字典"]
  end

  [frontmatter, content, []]
end

def validate_frontmatter(skill_dir, skill_md_path, frontmatter, content)
  errors = []

  unexpected_keys = frontmatter.keys.map(&:to_s) - ALLOWED_FRONTMATTER_KEYS
  unless unexpected_keys.empty?
    errors << "#{skill_md_path}: frontmatter 只允许 #{ALLOWED_FRONTMATTER_KEYS.join('/')}，发现额外字段: #{unexpected_keys.sort.join(', ')}"
  end

  name = frontmatter["name"]
  if !name.is_a?(String) || name.strip.empty?
    errors << "#{skill_md_path}: frontmatter 缺少有效的 name"
  else
    name = name.strip
    errors << "#{skill_md_path}: name 只能包含小写字母、数字和连字符" unless name.match?(/\A[a-z0-9-]+\z/)
    errors << "#{skill_md_path}: name 不能以前后连字符开头结尾，也不能出现连续连字符" if name.start_with?("-") || name.end_with?("-") || name.include?("--")
    errors << "#{skill_md_path}: name 长度不能超过 #{MAX_SKILL_NAME_LENGTH}" if name.length > MAX_SKILL_NAME_LENGTH
    errors << "#{skill_md_path}: name 需要与目录名一致，当前为 #{name}，目录为 #{skill_dir.basename}" unless name == skill_dir.basename.to_s
  end

  description = frontmatter["description"]
  if !description.is_a?(String) || description.strip.empty?
    errors << "#{skill_md_path}: frontmatter 缺少有效的 description"
  else
    description = description.strip
    errors << "#{skill_md_path}: description 不能包含尖括号" if description.include?("<") || description.include?(">")
    errors << "#{skill_md_path}: description 长度不能超过 #{MAX_DESCRIPTION_LENGTH}" if description.length > MAX_DESCRIPTION_LENGTH
  end

  body = content.sub(FRONTMATTER_PATTERN, "")
  errors << "#{skill_md_path}: frontmatter 后缺少正文" if body.strip.empty?
  errors
end

def validate_openai_yaml(skill_dir, skill_name)
  openai_yaml_path = skill_dir + "agents/openai.yaml"
  return [] unless openai_yaml_path.exist?

  begin
    data = YAML.safe_load(read_text(openai_yaml_path), permitted_classes: [], aliases: false)
  rescue Psych::Exception => e
    return ["#{openai_yaml_path}: YAML 无法解析: #{e.message.lines.first&.strip}"]
  end

  unless data.is_a?(Hash)
    return ["#{openai_yaml_path}: 顶层必须是 YAML 字典"]
  end

  errors = []
  interface = data["interface"]
  policy = data["policy"]

  unless interface.is_a?(Hash)
    errors << "#{openai_yaml_path}: 缺少 interface 字典"
    return errors
  end

  %w[display_name short_description default_prompt].each do |key|
    value = interface[key]
    errors << "#{openai_yaml_path}: interface.#{key} 缺失或为空" unless value.is_a?(String) && !value.strip.empty?
  end

  unless policy.is_a?(Hash)
    errors << "#{openai_yaml_path}: 缺少 policy 字典"
    return errors
  end

  allow_implicit = policy["allow_implicit_invocation"]
  unless allow_implicit == true || allow_implicit == false
    errors << "#{openai_yaml_path}: policy.allow_implicit_invocation 必须是布尔值"
  end

  default_prompt = interface["default_prompt"]
  if default_prompt.is_a?(String) && !default_prompt.include?("$#{skill_name}")
    errors << "#{openai_yaml_path}: interface.default_prompt 需要显式包含 $#{skill_name}"
  end

  errors
end

def validate_skill(skill_dir)
  skill_md_path = skill_dir + "SKILL.md"
  return ["#{skill_dir}: 缺少 SKILL.md"] unless skill_md_path.exist?

  frontmatter, content, errors = parse_frontmatter(skill_md_path)
  return errors unless errors.empty?

  errors = validate_frontmatter(skill_dir, skill_md_path, frontmatter, content)
  errors.concat(validate_openai_yaml(skill_dir, frontmatter["name"].to_s.strip))
  errors
end

def main
  target = Pathname.new(ARGV[0] || Pathname(__dir__).parent.to_s).expand_path
  skill_dirs = find_skill_dirs(target)
  if skill_dirs.empty?
    warn("错误: 在 #{target} 下没有找到可校验的 skill")
    return 1
  end

  errors = skill_dirs.flat_map do |skill_dir|
    validate_skill(skill_dir).map { |message| "[#{skill_dir.basename}] #{message}" }
  end

  if errors.empty?
    puts("通过: SKILL.md 最终校验完成，共校验 #{skill_dirs.length} 个 skill")
    return 0
  end

  errors.each { |message| warn("错误: #{message}") }
  1
end

exit(main)
