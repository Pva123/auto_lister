# Auto Lister

Simple automation tool to manage second-hand item listings across Facebook Marketplace, Kijiji, and eBay.

## Setup

1. **Create virtual environment (recommended):**

   ```bash
   python -m venv auto_lister_env
   source auto_lister_env/bin/activate  # On macOS/Linux
   # auto_lister_env\Scripts\activate   # On Windows
   ```

2. **Install dependencies:**

   ```bash
   python setup.py
   ```

3. **Add your items:**
   - Create folders in `items/` (e.g., `items/my_laptop/`)
   - Add `info.json` with item details
   - Add product images
   - See `items/sample_item/` for example

## Usage

```bash
python lister.py
```

The tool will:

- Check each platform for existing listings
- Prompt you to post missing items
- Auto-fill forms (you complete manually)
- Save login sessions for next time

## Item Structure

Each item folder needs an `info.json`:

```json
{
  "title": "Vintage Leather Jacket - Size M",
  "description": "Beautiful vintage leather jacket...",
  "price": 85,
  "platforms": ["facebook", "kijiji"],
  "category": "Clothing",
  "condition": "Used - Excellent"
}
```

## Files

- `setup.py` - One-time setup script
- `lister.py` - Main automation script
- `items/` - Your items database
- `browser_data/` - Saved login sessions (auto-created)

That's it! Simple and minimal.
