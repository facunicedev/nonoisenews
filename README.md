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

A minute and a half, from the questionnaire to your first paper (click to play):



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

You don't need to know anything about computers. There are three things to do; Claude takes care of the rest.

1. **Install Claude.** Go to [claude.ai/download](https://claude.ai/download), download it for Windows, open it and sign in. You need a paid plan (Pro or Max).
2. **Download No Noise News.** On this page, at the top, click the green **Code** button and then **Download ZIP**. When it finishes, go to your Downloads folder, right-click the file and choose **Extract All**. Put the folder wherever you like, for example in Documents.
3. **Open it with Claude.** Double-click **Abrir con Claude** inside the folder: the Claude app opens on it with a greeting typed in, so just press Enter. If that doesn't work, open the Claude app, go to the **Code** tab at the top, choose the folder and type **hi**.

From there, Claude sets up your computer on its own (it installs whatever is needed, even if you don't know what it is). When it asks for permission to do something, click **Allow**. The page opens on the right with a short questionnaire; save it and press **Brief me**.

To read your stories without opening Claude, double-click **Abrir** inside the folder. It opens in your browser; close the small black window to switch it off. The buttons only work while Claude is open.

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
