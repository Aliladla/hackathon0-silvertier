# Bronze Tier Personal AI Employee

A foundational Personal AI Employee system that monitors a local folder for dropped files, creates action items in an Obsidian vault, and enables Claude Code to read and process those items.

## Features (Bronze Tier)

- **File Monitoring**: Automatically detects files dropped into Inbox folder
- **Action Item Creation**: Creates structured markdown files in Needs_Action folder
- **Dashboard View**: Visual status overview in Obsidian
- **AI Processing**: Claude Code Agent Skills for processing action items
- **Behavior Rules**: Customizable AI behavior through Company_Handbook.md
- **Audit Logging**: All operations logged with timestamps

## Prerequisites

- Python 3.13 or higher
- [Obsidian](https://obsidian.md/download) v1.10.6+
- [Claude Code](https://claude.com/product/claude-code) (active subscription or free Gemini API)
- Git (for version control)

## Installation

### 1. Clone Repository

```bash
git clone <repository-url>
cd hackathon0ali
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and set your vault path
# VAULT_PATH=C:\Users\YourName\Desktop\hackathon0ali\AI_Employee_Vault
```

### 4. Open Obsidian Vault

1. Open Obsidian
2. Click "Open folder as vault"
3. Select `AI_Employee_Vault` folder
4. Review `Dashboard.md` and `Company_Handbook.md`

## Usage

### Start the File Watcher

```bash
python src/main.py
```

The watcher will monitor `AI_Employee_Vault/Inbox/` for new files.

### Drop Files for Processing

1. Drop any file into `AI_Employee_Vault/Inbox/`
2. Within 5 seconds, an action item appears in `Needs_Action/`
3. Open Obsidian to see the new item in Dashboard

### Process with Claude Code

```bash
# Navigate to vault directory
cd AI_Employee_Vault

# Run Claude Code with process_action skill
claude code

# In Claude Code, use the skill:
/process_action
```

Claude will read files from `Needs_Action/`, check `Company_Handbook.md` rules, and provide processing recommendations.

### Move Completed Items

After processing, use the move_to_done skill:

```bash
# In Claude Code:
/move_to_done <filename>
```

Or manually move files from `Needs_Action/` to `Done/`.

## Project Structure

```
hackathon0ali/
├── AI_Employee_Vault/          # Obsidian vault
│   ├── Inbox/                  # Drop zone for files
│   ├── Needs_Action/           # Action items (auto-created)
│   ├── Done/                   # Completed tasks
│   ├── Errors/                 # Failed processing
│   ├── Logs/                   # System logs
│   ├── Dashboard.md            # Status overview
│   └── Company_Handbook.md     # AI behavior rules
├── src/
│   ├── watchers/
│   │   ├── base_watcher.py     # Abstract base class
│   │   └── file_watcher.py     # File system watcher
│   ├── utils/
│   │   ├── logger.py           # Logging utilities
│   │   └── vault_manager.py    # Vault operations
│   └── main.py                 # Entry point
├── .claude/
│   └── skills/                 # Claude Code Agent Skills
│       ├── process_action.md
│       ├── update_dashboard.md
│       ├── move_to_done.md
│       └── check_handbook.md
├── specs/                      # SDD artifacts
│   └── bronze-ai-employee/
│       ├── spec.md
│       ├── plan.md
│       └── tasks.md
├── requirements.txt
├── .env.example
└── README.md
```

## Configuration

### Environment Variables (.env)

- `VAULT_PATH`: Absolute path to Obsidian vault
- `DRY_RUN`: Set to `true` for Bronze tier (no external actions)
- `CHECK_INTERVAL`: File watcher check interval in seconds (default: 30)
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

### Company Handbook Rules

Edit `AI_Employee_Vault/Company_Handbook.md` to customize AI behavior:

```markdown
## Rules

- Flag all invoices over $500 for review
- Prioritize client emails within 24 hours
- Log all financial documents to accounting folder
```

## Troubleshooting

### Watcher Not Detecting Files

- Verify `VAULT_PATH` in `.env` is correct
- Check that `Inbox/` folder exists
- Review logs in `AI_Employee_Vault/Logs/`

### Claude Code Can't Read Vault

- Ensure you're running Claude Code from the vault directory
- Verify file permissions allow read access
- Check that `.obsidian/` folder exists (created by Obsidian)

### Files Not Appearing in Dashboard

- Manually refresh Dashboard.md in Obsidian
- Run `/update_dashboard` skill in Claude Code
- Check watcher logs for errors

## Bronze Tier Limitations

- Manual dashboard refresh (auto-refresh in Silver+)
- Single file watcher (Gmail/WhatsApp in Silver+)
- No automated external actions (email, payments in Gold+)
- Manual testing only (automated tests in Silver+)

## Next Steps

After completing Bronze tier:

1. **Silver Tier**: Add Gmail/WhatsApp watchers, MCP servers, automated scheduling
2. **Gold Tier**: Full cross-domain integration, weekly audits, Ralph Wiggum loop
3. **Platinum Tier**: Cloud deployment, 24/7 operation, always-on monitoring

## License

MIT License - See LICENSE file for details

## Contributing

This is a hackathon project. Contributions welcome via pull requests.

## Support

- Join Wednesday Research Meetings: [Zoom Link](https://us06web.zoom.us/j/87188707642?pwd=a9XloCsinvn1JzICbPc2YGUvWTbOTr.1)
- Watch recordings: [YouTube](https://www.youtube.com/@panaversity)
- Submit issues: GitHub Issues
