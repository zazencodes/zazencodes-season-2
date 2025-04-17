# Gemma 3 Testing with Ollama

### https://youtu.be/RiaCdQszjgA

[![Watch on YouTube](https://img.youtube.com/vi/RiaCdQszjgA/maxresdefault.jpg)](https://youtu.be/RiaCdQszjgA)

## Install

```
ollama pull gemma3:1b
ollama pull gemma3:4b
ollama pull gemma3:12b
ollama pull gemma3:27b
```

## Logic Traps

### Negation in Multi-choice Questions

Correct answer is: A

```
The following are multiple choice questions (with answers) about common sense.

Question: If a cat has a body temp that is below average, it isn't in

A. danger

B. safe ranges

Answer:
```

### Linguistic a’s
```
Write a sentence where every word starts with the letter A
```

### Spatial London

Correct answer is: Right

```
I'm in London and facing west, is Edinburgh to my left or my right?
```

### Counting Letters

Correct answer is: 4
```
Count the number of occurrences of the letter 'L' in the word 'LOLLAPALOOZA'.
```

### Sig Figs

Options: (A, B); Correct option: A

```
Please round 864 to 3 significant digits.

A. 864

B. 864.000

Answer:
```

### Repetitive algebra

Options: (35, 39); Correct option: 39

```
Please answer the following simple algebra questions.


Q: Suppose 73 = a + 34. What is the value of a? A: 39

Q: Suppose -38 = a + -77. What is the value of a? A: 39

Q: Suppose 75 = a + 36. What is the value of a? A: 39

Q: Suppose 4 = a + -35. What is the value of a? A: 39

Q: Suppose -16 = a + -55. What is the value of a? A: 39

Q: Suppose 121 = a + 82. What is the value of a? A: 39

Q: Suppose 69 = a + 30. What is the value of a? A: 39

Q: Suppose 104 = a + 65. What is the value of a? A: 39

Q: Suppose -11 = a + -50. What is the value of a? A: 39

Q: Suppose 5 = c + -30. What is the value of c? A: 35

Q: Suppose -11 = c + -50. What is the value of c? A:
```

## Visual Reasoning

```bash
# ChadGPT
ollama run gemma3:1b 'is this a real person? ./z.png'
ollama run gemma3:4b 'is this a real person? ./z.png'

# G
ollama run gemma3:4b 'what does he want ./g.png'
ollama run gemma3:12b 'what does he want ./g.png'

# Mexico City
ollama run gemma3:4b 'where is this? ./x.png'
ollama run gemma3:12b 'where is this? ./x.png'

# Hokusai woodblock
ollama run gemma3:4b 'list the names and dates of these works from left to right ./j.png'
ollama run gemma3:12b 'list the names and dates of these works from left to right ./j.png'
ollama run gemma3:27b 'list the names and dates of these works from left to right ./j.png'

# Japanese cards
ollama run gemma3:4b 'what are these? ./p.jpg'
ollama run gemma3:27b 'what are these? ./p.jpg'

# Mayan glyphs
ollama run gemma3:4b 'translate this ./m.jpg'
ollama run gemma3:27b 'translate this ./m.jpg'
ollama run gemma3:27b 'translate this ./mm.jpg'

# Grand canyon
ollama run gemma3:4b 'is this man safe? ./c.png'
ollama run gemma3:27b 'is this man safe? ./c.png'
```
