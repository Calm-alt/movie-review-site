# The Watch List

A one-page personal movie/series review site. Add a poster, a title, a
verdict (Must Watch / Watchable / Skip It), a quick take, and optionally
a longer write-up that expands in place under "Show more" — no page
navigation, everything lives on `/`.

## Run it in VS Code

1. Open this folder in VS Code.
2. Open a terminal (`` Ctrl+` ``) and create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate it:
   - macOS / Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   python app.py
   ```
6. Open the link it prints (usually `http://127.0.0.1:5000`) in your browser.

That's it — no separate database setup needed. A `reviews.db` SQLite file
is created automatically the first time you run the app, and uploaded
posters are saved to `static/uploads/`.

## Notes

- Max upload size is 8 MB per image; supported formats: png, jpg, jpeg, gif, webp.
- To reset everything, stop the server and delete `reviews.db` (and
  optionally clear out `static/uploads/`).
- To deploy this somewhere permanent later (e.g. PythonAnywhere, Render,
  Railway), you'd swap `app.run(debug=True)` for a production server, but
  for local personal use this is all you need.
