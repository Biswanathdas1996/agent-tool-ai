import React, { useState, useEffect } from "react";
import { Card, CardContent } from "@mui/material";
import Button from "@mui/material/Button";
import FormControlLabel from "@mui/material/FormControlLabel";
import Checkbox from "@mui/material/Checkbox";
import Loader from "../components/Loader";

const API_KEY = "AIzaSyB6SXZ8k-Otk4NmfFvXK6lzqqRCScksku4";
const API_URL = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;

interface Question {
  question: string;
  options: string[];
  correctAnswer: string;
}

const Chatbot: React.FC = () => {
  const [loading, setLoading] = useState<boolean>(false);
  const [chat, setChat] = useState<
    {
      question: string;
      options: string[];
      userAnswer?: string;
      correctAnswer: string;
      score: number;
    }[]
  >(() => {
    try {
      const storedChat = localStorage.getItem("chatHistory");
      return storedChat ? JSON.parse(storedChat) : [];
    } catch (error) {
      console.error("Error parsing chat history:", error);
      return [];
    }
  });
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);

  useEffect(() => {
    if (!chat.length) fetchQuestion();
  }, []);

  useEffect(() => {
    localStorage.setItem("chatHistory", JSON.stringify(chat));
  }, [chat]);

  const fetchQuestion = async () => {
    setLoading(true);
    try {
      const storedPrompt = `Generate a multiple-choice ${localStorage.getItem(
        "questionPrompt"
      )} question in valid JSON format.
       Do not repeat the previous question. 
      Response format:
  {
    "question": "What is ${localStorage.getItem("questionPrompt")}?",
    "options": ["A programming language", "A coffee brand", "A database", "An operating system"],
    "correctAnswer": "A programming language"
  }`;

      const response = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: storedPrompt,
                },
              ],
            },
          ],
        }),
      });

      const data = await response.json();
      let jsonResponse =
        data?.candidates?.[0]?.content?.parts?.[0]?.text || "{}";
      jsonResponse = jsonResponse.replace(/^```json|```/g, "").trim();
      const parsedQuestion: Question = JSON.parse(jsonResponse);

      // Check if the question already exists in the chat history
      const isDuplicate = chat.some(
        (entry) => entry.question === parsedQuestion.question
      );

      if (isDuplicate) {
        // If duplicate, fetch a new question
        fetchQuestion();
      } else {
        setCurrentQuestion(parsedQuestion);
      }

      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error("Failed to fetch question:", error);
    }
  };

  const checkAnswer = (selectedOption: string) => {
    if (!currentQuestion) return;
    const score = selectedOption === currentQuestion.correctAnswer ? 10 : 0;
    const newChat = [
      ...chat,
      {
        question: currentQuestion.question,
        options: currentQuestion.options,
        userAnswer: selectedOption,
        correctAnswer: currentQuestion.correctAnswer,
        score,
      },
    ];
    setChat(newChat);
    fetchQuestion();
  };

  const resetChat = () => {
    setChat([]);
    localStorage.removeItem("chatHistory");
    fetchQuestion();
  };

  return (
    <div>
      <h2 className="text-xl font-bold">
        {localStorage.getItem("questionPrompt")} Q&A Bot
      </h2>
      <div className="overflow-y-auto max-h-96 p-2 border rounded-lg">
        {Array.isArray(chat) && chat.length > 0 ? (
          chat.map((entry, index) => (
            <Card
              className="max-w-lg mx-auto mt-10 p-4"
              style={{ border: "1px solid rgb(0 0 0 / 9%)", marginTop: 20 }}
            >
              <CardContent>
                <div key={index} className="mb-4 p-2 border rounded-md">
                  <p
                    className="font-semibold"
                    style={{ fontSize: 20, fontWeight: 600 }}
                  >
                    {entry.question}
                  </p>
                  {entry?.options?.map((option, i) => (
                    <FormControlLabel
                      control={
                        <Checkbox
                          checked={option === entry.userAnswer}
                          disabled
                        />
                      }
                      label={
                        <span
                          className={`p-1 rounded ${
                            option === entry.correctAnswer
                              ? "bg-green-200"
                              : option === entry.userAnswer
                              ? "bg-red-200"
                              : ""
                          }`}
                        >
                          {option}
                        </span>
                      }
                      key={i}
                    />
                  ))}
                  <p className="text-sm text-gray-600">
                    Your Score: {entry.score}/10
                  </p>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <p>No previous chat history.</p>
        )}

        {loading ? (
          <Loader showIcon={false} />
        ) : (
          <>
            {currentQuestion && (
              <div className="mt-4 p-2 border rounded-md">
                <p
                  className="font-semibold"
                  style={{ fontSize: 20, fontWeight: 600 }}
                >
                  {currentQuestion.question}
                </p>
                {currentQuestion.options.map((option, index) => (
                  <FormControlLabel
                    control={
                      <Checkbox
                        onChange={() => checkAnswer(option)}
                        name={option}
                      />
                    }
                    label={<span style={{ color: "black" }}>{option}</span>}
                    key={index}
                    style={{
                      background: "#8080803d",
                      padding: 10,
                      borderRadius: 12,
                    }}
                  />
                ))}
              </div>
            )}
          </>
        )}
      </div>
      <Button
        onClick={resetChat}
        className="mt-4"
        variant="contained"
        color="warning"
        style={{ marginTop: 20 }}
      >
        Restart
      </Button>
    </div>
  );
};

export default Chatbot;
