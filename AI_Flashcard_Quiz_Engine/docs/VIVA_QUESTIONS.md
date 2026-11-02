# Viva Questions and Answers

1. **What is the project about?**  
   It converts lecture notes into flashcards, quizzes, scores, and explanations.

2. **Which backend framework is used?**  
   Flask, a lightweight Python web framework.

3. **Which database is used?**  
   SQLite, a file-based relational database.

4. **Why is SQLite suitable here?**  
   It is lightweight, serverless, portable, and requires no separate database server.

5. **Can the project run without an API key?**  
   Yes. The local NLP mode works completely offline.

6. **What file formats are supported?**  
   TXT, PDF, and DOCX.

7. **How is text extracted from PDF files?**  
   Using the PyPDF2 library.

8. **How is text extracted from DOCX files?**  
   Using the python-docx library.

9. **What is NLP?**  
   Natural Language Processing, a field of AI that enables computers to understand human language.

10. **What is tokenization?**  
   Breaking text into smaller units such as sentences or words.

11. **What are stop words?**  
   Common words such as “the”, “is”, and “and” that usually add little meaning.

12. **How are keywords identified?**  
   By removing stop words and ranking words using frequency analysis.

13. **How are definitions detected?**  
   Using patterns such as “X is…”, “X refers to…”, and “X means…”.

14. **How are important sentences selected?**  
   Using keyword density, sentence length, and position-based ranking.

15. **How are MCQ distractors created?**  
   From other extracted definitions and important keywords.

16. **What is a cloze question?**  
   A fill-in-the-blank question created by hiding an important keyword.

17. **How is quiz score calculated?**  
   Each correct selected answer adds one mark; percentage is score divided by total multiplied by 100.

18. **What is Flask?**  
   A Python micro web framework used to build web applications.

19. **What is a route in Flask?**  
   A URL pattern mapped to a Python function.

20. **What is Jinja2?**  
   Flask’s templating engine used to generate dynamic HTML.

21. **What is `url_for()`?**  
   A Flask function that generates URLs for routes and static files.

22. **What is `render_template()`?**  
   A Flask function that renders an HTML template with dynamic data.

23. **What is SQLite foreign key?**  
   A column that links records in one table to records in another table.

24. **What is SQL injection?**  
   An attack where malicious SQL is inserted into queries. This project uses parameterized queries to prevent it.

25. **How are uploaded filenames secured?**  
   Using Werkzeug’s `secure_filename()` function.

26. **Why is upload size limited?**  
   To prevent memory and storage abuse from very large files.

27. **Why are uploaded files deleted after parsing?**  
   To avoid storing unnecessary user files on the server.

28. **What is Bootstrap?**  
   A CSS framework used for responsive layouts and UI components.

29. **How does the flashcard flip animation work?**  
   CSS 3D transforms rotate the card using `rotateY(180deg)`.

30. **What is the difference between MCQ and true/false questions?**  
   MCQs have four options; true/false questions have only two options.

31. **What is overfitting in AI?**  
   When a model learns training data too specifically and performs poorly on new data.

32. **What is machine learning?**  
   A subset of AI where systems learn patterns from data.

33. **What is the difference between AI and ML?**  
   AI is the broader field of intelligent behavior; ML is a method of learning from data.

34. **What is an API?**  
   An Application Programming Interface that allows software systems to communicate.

35. **How does AI Mode work?**  
   It sends cleaned notes to an OpenAI-compatible API and expects structured JSON study material.

36. **What happens if AI Mode fails?**  
   The application falls back to the local NLP generator.

37. **What is normalization in databases?**  
   Organizing data to reduce duplication and improve integrity.

38. **Why is JSON used in the database?**  
   To store quiz options and submitted answers compactly.

39. **What is a virtual environment?**  
   An isolated Python environment containing project-specific packages.

40. **What are future enhancements?**  
   OCR, login accounts, spaced repetition, PDF export, and semantic AI generation.
