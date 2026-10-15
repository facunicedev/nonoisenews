<p align="center">
  <img src="web/icono.png" alt="No Noise News" width="140">
</p>

<h1 align="center">No Noise News</h1>

<p align="center">
  <b>Your paper today, written for you.</b><br>
  A daily news briefing that runs on your own computer with Claude. You tell it what you care about; it searches, picks the stories that matter to you and writes them up in ten minutes of reading.
</p>

<p align="center">
  <b>English</b> · <a href="README.es.md">Español</a>
</p>

<p align="center">
  <img src="docs/story.png" alt="A story in No Noise News" width="820">
</p>

## Demo

A minute and a half, from the questionnaire to your first paper:

https://github.com/user-attachments/assets/ea7cb2fc-d309-4fa4-813f-0ee2ffd23ade

## What it does

- **Only your news.** A short questionnaire: how many stories, which topics and how much each one weighs (*Always*, *More*, *Normal*, *Less*, *Never*), and anything else in your own words.
- **Written for you, not copied.** Claude reads the news from the last 24-48 hours and writes each story itself: what happened, the minimum context and why it matters to you. The key sentences are in bold, so you can skim.
- **Always with sources.** At least two per story, marked as free or paywalled. Nothing is made up: no figures, quotes or links it hasn't read.
- **Ask about anything.** Under each story, «Tell me more» digs deeper and «Ask me» answers whatever you didn't understand, like a smart friend would.
- **Learns from you.** «Not interested», with an optional reason, shapes the next briefing.
- **The big picture.** A separate tab with how the world stands: the big global stories, the countries you follow and the key indicators (oil, rates, inflation, markets), each with one sentence explaining whether it's good or bad.
- **In your language.** English, Spanish, French and German. Switch it and your stories are translated.

## How it works

You talk to Claude in the Claude app; No Noise News is the page next to it, where you read and press buttons. Each button tells Claude what to do: «Brief me» brings today's stories, «Tell me more» expands one, «Ask me» answers a question. Everything stays on your computer.

## Getting started

You don't need to know anything about computers. It takes about ten minutes the first time, and Claude does the technical part for you.

### What you need

- **A Windows computer.**
- **A paid Claude plan (Pro or Max).** No Noise News runs on Claude Code, which comes included in those plans; the free plan doesn't include it. You can subscribe at [claude.ai](https://claude.ai).

### Step by step

1. **Install the Claude app.** Go to [claude.ai/download](https://claude.ai/download), download the Windows version, install it and sign in with your account.
2. **Download No Noise News.** Click here: **[NoNoiseNews.zip](https://github.com/facunicedev/nonoisenews/releases/latest/download/NoNoiseNews.zip)**.
3. **Unzip it.** Go to your **Downloads** folder, right-click the file `NoNoiseNews.zip` and choose **Extract All** → **Extract**. A folder called `NoNoiseNews` appears. Move it wherever you like, for example to **Documents**. That folder is your No Noise News: don't delete it, your news and settings live there.
4. **Open the folder in Claude.** Open the Claude app and click **Code** at the top. Click the folder selector, choose the No Noise News folder you just unzipped and confirm. If Claude asks whether you trust the folder, say yes.
   *Shortcut:* double-click **Abrir con Claude** inside the folder and it opens there by itself.
5. **Say hi.** Type **hi** in the chat and press Enter. Claude sets up your computer on its own (if Python is missing, it installs it). Whenever it asks for permission, click **Allow**.
6. **The page opens next to the chat.** On the right side of the Claude window you'll see No Noise News with a short questionnaire: your language, how many stories, your topics. Fill it in and click **Save**. (If it doesn't appear on the right, Claude opens it in your browser instead.)
7. **Press «Brief me».** Claude searches the news and writes your paper. It takes a few minutes; when it's ready, the page updates by itself.

### Every day after that

Open the Claude app, go to **Code**, pick the No Noise News folder and say **hi**. The page opens on the right; press **Brief me**. If you ticked «Shall I fetch them on my own?» in *Your search*, you don't even need to press it.

To read your stories without opening Claude, double-click **Abrir** inside the folder: they open in your browser. Close the small black window to switch it off. The buttons only work while Claude is open.

## The page

| Tab | What you find there |
|---|---|
| **Home** | The essentials of the day and your stories, one per card, with their sources and the «Tell me more», «Not interested» and «Ask me» buttons. |
| **The big picture** | How the world stands: indicators with a plain-language reading, and the big stories by area (global and the countries you follow). |
| **Your search** | Your language, how many stories, your topics and their weight, and whether it should fetch the news on its own when you open Claude. |

<p align="center">
  <img src="docs/big-picture.png" alt="The big picture" width="410">
  <img src="docs/your-search.png" alt="Your search" width="410">
</p>

It also has a night mode.

<p align="center">
  <img src="docs/story-dark.png" alt="Night mode" width="820">
</p>

## Updates

Once a week, when you open it, Claude checks this page for a new version and updates itself. Your data (profile, stories) is never touched. You can also ask it: «update».

## Your data

Everything stays on your computer, in the `datos/` folder, which never goes to GitHub. The page only works on your own computer.

## Project structure

| File | What it is |
|---|---|
| `CLAUDE.md` | Claude's instructions: how it talks to you, how it picks and writes the stories (in Spanish). |
| `panel.py` | The small local server behind the page; it records each button for Claude. No dependencies beyond Python. |
| `web/` | The page itself. |
| `.claude/` | Settings, the weekly update skill and the page preview for the Claude app. |
| `Abrir con Claude.bat`, `Abrir.bat` | Shortcuts: open with Claude, or just the page. |

## License

MIT. See [`LICENSE`](LICENSE).
