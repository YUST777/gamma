with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md') as f:
    text = f.read()

text = text.replace(
    'Deleted  from the cover header: now strictly ****.',
    'Deleted `& ENGINEERING` from the cover header: now strictly **`FACULTY OF ARTIFICIAL INTELLIGENCE`**.'
)
text = text.replace(
    'Restored photo height to **300px** with balanced vertical centering (), matching the pre-index framing.',
    'Restored photo height to **300px** with balanced vertical centering (`object-position: center 45%`), matching the pre-index framing.'
)

with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md', 'w') as f:
    f.write(text)

print('Done fixing walkthrough')
