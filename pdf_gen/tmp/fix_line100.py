with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md') as f:
    text = f.read()

text = text.replace(
    'Deleted  from the cover header: now strictly .',
    'Deleted `& ENGINEERING` from the cover header: now strictly **`FACULTY OF ARTIFICIAL INTELLIGENCE`**.'
)

with open('/home/yousefmsm1/.gemini/antigravity/brain/8d42f6dc-2245-44cf-8d50-2f03b9093fe9/walkthrough.md', 'w') as f:
    f.write(text)

print('Line 100 fixed')
