# Claude Code Subagent Collection

This directory contains specialized subagents and a builder system based on lessons learned from creating the Excel data analyzer.

## 🎯 Available Subagents

### 1. **data-analyzer** - Universal Data Analysis
- Analyzes ANY file type (Excel, CSV, JSON, text, images, databases, code)
- Direct bash execution with `uv run python -c` commands
- Data quality assessment, missing values, text issues
- Multi-format conversion capabilities
- **Usage**: Invoke with Task tool for any data analysis needs

### 2. **subagent-builder** - Subagent Generator  
- Builds new specialized subagents based on your requirements
- Incorporates best practices learned from our experience
- Templates for data, code, security, file processing, DevOps agents
- **Usage**: Ask it to build any type of specialized analyzer you need

## 🛠️ Builder System Architecture

### Core Files:
- `subagent-builder.md` - Main builder that creates new agents
- `subagent_templates.md` - Template library with patterns for different agent types
- `data-analyzer.md` - Universal data analyzer (example of best practices)

### Key Design Principles Learned:

#### ✅ **Direct Execution** (Critical!)
- Always use `uv run python -c "..."` for immediate results
- NEVER create Python script files (wastes tokens)
- Focus on bash commands with inline Python

#### ✅ **Token Efficiency**
- Separate context windows save main agent tokens
- Compressed, structured outputs
- Specialized system prompts for focused tasks

#### ✅ **YAML Frontmatter Structure**
```yaml
---
name: agent-name
description: Clear description of purpose and when to invoke
tools: Read, Write, Bash, Glob, LS, Grep
---
```

#### ✅ **Directive System Prompts**
- Start with clear role definition
- Include "CRITICAL INSTRUCTION" sections
- Provide bash command templates
- Specify response format
- Include dependency management

## 🚀 How to Use

### Create a New Subagent:
1. Invoke the subagent-builder: 
   ```
   Use the subagent-builder to create a [type] analyzer for [purpose]
   ```

2. It will ask clarifying questions and generate the complete agent file

3. Test the new agent by invoking it with the Task tool

### Example Usage:
```
Use the subagent-builder to create a log file analyzer for web server access logs

Use the data-analyzer to analyze the Excel file at /path/to/data.xlsx

Use the python-analyzer (if built) to audit the code quality in this project
```

## 📋 Agent Types Available for Building

### Data & Analytics:
- CSV/Excel analyzers
- Database schema analyzers  
- Statistical analysis agents
- Time series analyzers
- Data quality assessors

### Code Analysis:
- Language-specific analyzers (Python, JavaScript, Java, etc.)
- Security vulnerability scanners
- Code quality metrics
- Dependency analyzers
- Documentation generators

### File Processing:
- Log analyzers (access logs, application logs, system logs)
- Image processors
- Document converters
- Archive handlers

### Security & Compliance:
- Security auditors
- Configuration validators
- Permission analyzers
- Credential scanners

### Infrastructure & DevOps:
- Docker/container analyzers
- CI/CD pipeline validators
- System monitoring agents
- Performance profilers

## 💡 Best Practices (Learned from Experience)

1. **Always emphasize direct execution** in agent prompts
2. **Provide specific bash command examples** for common tasks
3. **Include dependency installation** commands (uv add packages)  
4. **Structure responses consistently** with clear sections
5. **Focus on actionable insights** rather than raw data dumps
6. **Handle edge cases** and error scenarios
7. **Keep agents specialized** rather than trying to do everything

## 🔧 Technical Notes

- Agents are automatically discovered by Claude Code when placed in `.claude/agents/`
- Use descriptive names and clear descriptions for easy invocation
- Test agents with sample data before using in production
- Update dependencies as needed with `uv add package_name`

## 📚 References

- [Claude Code Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [MCP Integration Guide](https://docs.anthropic.com/en/docs/claude-code/mcp)

---

**Built from our Excel analyzer journey** - incorporating lessons learned about token efficiency, direct execution, and specialized analysis capabilities.