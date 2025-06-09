# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Universal Project Framework

This repository contains the Universal Project Framework v1.0 - a comprehensive development framework optimized for Claude Desktop + MCP environment projects.

### Framework Components

1. **universal_project_framework.md** - Core framework with Phase-Q Template (7-stage development phases)
2. **enterprise_prediction_project_rules.md** - Specialized rules for AI/ML prediction systems 
3. **project_config_templates.md** - Project type-specific configuration templates
4. **implementation_examples.md** - Real implementation examples and best practices

### Development Philosophy

- **Quality First**: Maintain 0% error rate and perfect UTF-8 character encoding
- **Phase-Driven**: Follow 7-stage development phases with quality gates
- **Documentation-Centric**: Record all progress and decisions systematically
- **Reusability**: Create templates and patterns for efficient project setup

### Key Principles

1. **Essential Function Priority**: Focus on core functionality before UI/UX
2. **Staged Implementation**: Requirements → Design → Code progression
3. **Quality Gates**: Mandatory quality checks at each phase completion
4. **Progress Recording**: Systematic documentation of all phases and decisions

### Quality Standards

- **Error Rate**: 0% tolerance for errors across all development stages
- **Character Encoding**: UTF-8 complete unification, 0% character corruption
- **Performance**: Environment-specific optimization (Windows primary)
- **Reproducibility**: Ensure reliable reproduction in other environments

### Framework Usage

When starting any new project:

1. Select appropriate config template from `project_config_templates.md`
2. Apply Universal Framework principles from `universal_project_framework.md`
3. Follow specialized rules if applicable (e.g., AI/ML systems)
4. Reference implementation examples for proven patterns
5. Maintain systematic progress records throughout development

### GitHub Security & Compliance Rules

**MANDATORY for ALL GitHub public projects:**

Before any commit to public repositories, MUST complete:

1. **Security Check (GITHUB_SECURITY_RULES.md)**:
   - Remove ALL API keys, personal info, real logs, test data
   - Verify no sensitive information in code, comments, or files
   - Implement environment variable configuration
   - Add appropriate .gitignore and security documentation

2. **Compliance Check**:
   - Verify commercial use compatibility for all data sources
   - Add required attributions and source citations
   - Confirm license compatibility
   - Document data source usage in README.md

**Zero tolerance policy**: No exceptions for security and compliance violations.

### MCP Integration

Optimized for Claude Desktop with recommended MCP extensions:
- **filesystem**: Large file operations and log management
- **sequential-thinking**: Complex problem step-by-step resolution
- **memory**: Project history and configuration storage
- **brave_web_search**: Latest technology information and competitive research

This framework ensures high-quality, efficient development across any project type while maintaining systematic documentation and reproducible results.