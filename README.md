# Full Stack API Final Project

## Full Stack Trivia

this project was part of Full-Stack Nanodegree from Udacity .
Trivia_API is an API that allows the user to access trivia database to get , post and delete question and categorize it by question category. The application allows the user:

1. Display questions - both all questions and by category. Questions shows the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Setup

First you need to setup the backend by folowing the instraction in [Backend README](./backend/README.md).
Affter that you can use the API from your website or by the frontend that is in /frontend file,to setup the frontend see [frontend README](./frontend/README.md).

## API Reference

### Geting Starting

Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:

```bash
{
"success": False,
"error": 400,
"message": "bad request"
}
```

The API will return three error types when requests fail:

400: Bad Request
404: Resource Not Found
405: Method Not Allowed
422: Not Processable

in addition to some error that is being handeled but for now the API is not returning it:

401: Unauthorized
500: Internal Server Error

### End Points

GET /categories
General:
Returns a list of categories objects and success value
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/categories

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

GET /categories/{int:category_id}/questions
General:
Returns a list of question objects, success value, categories list, total number of questions and the ID for the category
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/categories/2/questions

```bash
{
  "current_category": 3,
  "questions": [
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "total_questions": 3
}

```

---

GET /questions
General:
Returns a list of question objects, success value, categories list, and total number of questions
Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1.
Sample: curl http://127.0.0.1:5000/questions

```bash
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    },
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    }
  ],
  "success": true,
  "total_questions": 24
}
```

POST /questions
General:
Creates a new question using the submitted question, answer, difficulty and category. Returns the id of the created book and success value. searchTerm must be NULL of it will return search results
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{question: "What is the name of this API creater", answer: "Abdulaziz Alasiri", difficulty: 1, category: 1}'

```bash
{
  "created": 45,
  "success": true
}

```

General:
Search for the questions contaning the String provaided in searchTerm .Returns al list of questions ,success value, and total number of questions.
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{searchTerm: "name of this API"}'

```bash
{
  "currentCategory": null,
  "questions": [
    {
      "answer": "Abdulaziz Alasiri",
      "category": 1,
      "difficulty": 1,
      "id": 46,
      "question": "What is the name of this API creater"
    }
  ],
  "success": true,
  "total_questions": 1
}
```

DELETE /questions/{int:question_id}
General:

Deletes the question with the provided ID .Returns the ID ro the deleted question and success value.
curl http://127.0.0.1:5000/questions/45 -X DELETE -H "Content-Type: application/json"

```bash
{
    "deleted": 45,
    "success": true
    }
```

POST /quizzes
General:
Creates a new quiz using the submitted previous questions and category. Returns a question that is not in the previous questions and success value.
curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{previous_questions: [13, 14], quiz_category: {type: "Geography", id: "3"}}'

```bash
{
  "question": {
    "answer": "Agra",
    "category": 3,
    "difficulty": 2,
    "id": 15,
    "question": "The Taj Mahal is located in which Indian city?"
  },
  "success": true
}

```

## Authors

[AbeFeinberg](https://github.com/AbeFeinberg).
[AbdulazizAlasiri](https://github.com/AbdulazizAlasiri)
