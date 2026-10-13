
import { useRef, useState } from "react";
import "./App.css";

const suggestions = [
  {
    icon: "अ",
    title: "संस्कृतेन सम्भाषामहे",
    subtitle: "Let us converse in Sanskrit",
    prompt: "नमस्ते",
  },
  {
    icon: "文",
    title: "Explore Sanskrit greetings",
    subtitle: "अभिवादनानि शिक्षस्व",
    prompt: "What are common Sanskrit greetings?",
  },
  {
    icon: "✳",
    title: "Learn a Sanskrit word",
    subtitle: "नूतनं शब्दं शिक्षस्व",
    prompt: "Teach me a new Sanskrit word",
  },
];

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const inputRef = useRef(null);
  const bottomRef = useRef(null);

  const hasMessages = messages.length > 0;

  async function sendMessage(text = input) {
    const message = text.trim();

    if (!message || loading) return;

    setMessages((current) => [
      ...current,
      { role: "user", content: message },
    ]);

    setInput("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/api/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ message }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.error || "Unable to send message."
        );
      }

      // Keep the typing indicator visible briefly.
      await new Promise((resolve) =>
        setTimeout(resolve, 550)
      );

      setMessages((current) => [
        ...current,
        {
          role: "assistant",
          content: data.reply,
          suggestions:
            data.suggestions ||
            data.reply.questions ||
            [],
        },
      ]);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Could not connect to Samvaad. Check that the Flask backend is running."
          : err.message ||
            "Something went wrong. Please try again."
      );
    } finally {
      setLoading(false);
      inputRef.current?.focus();

      setTimeout(() => {
        bottomRef.current?.scrollIntoView({
          behavior: "smooth",
          block: "end",
        });
      }, 100);
    }
  }

  function newChat() {
    setMessages([]);
    setInput("");
    setError("");
    inputRef.current?.focus();
  }

  function retryLastMessage() {
    const lastUserMessage = [...messages]
      .reverse()
      .find((message) => message.role === "user");

    if (lastUserMessage) {
      sendMessage(lastUserMessage.content);
    }
  }

  function renderAnswer(answer) {
    // Supports older string-only responses as well.
    const sanskrit =
      typeof answer === "string"
        ? answer
        : answer?.sanskrit || "";

    const english =
      typeof answer === "string"
        ? answer
        : answer?.english || "";

    return (
      <div className="bilingual-answer-grid">
        <div
          className="answer-column sanskrit-column"
          lang="sa"
          aria-label="Sanskrit response"
        >
          <p>{sanskrit}</p>
        </div>

        <div
          className="answer-column english-column"
          lang="en"
          aria-label="English translation"
        >
          <p>{english}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-symbol">सं</span>

          <span>
            <strong>Samvaad</strong>
            <small>संस्कृतसम्भाषणम्</small>
          </span>
        </div>

        <button className="new-chat" onClick={newChat}>
          <span>＋</span> New conversation
        </button>

        <div className="sidebar-label">YOUR SPACE</div>

        <div className="sidebar-note">
          <span className="note-icon">❋</span>
          <p>A little Sanskrit, a little every day.</p>
        </div>

        <div className="sidebar-bottom">
          <span className="online-dot" />
          <span>Guided Sanskrit chatbot</span>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div className="topbar-title">
            <span className="mobile-mark">सं</span>

            <div>
              <strong>संवादः</strong>
              <span>Your Sanskrit companion</span>
            </div>
          </div>

          <span className="bilingual-badge">
            <span>अ</span> Sanskrit + English
          </span>
        </header>

        <section
          className={`chat-area ${
            hasMessages ? "conversation" : ""
          }`}
        >
          {!hasMessages ? (
            <div className="welcome">
              <div className="welcome-emblem">
                <span>अ</span>
                <i>✳</i>
              </div>

              <div className="eyebrow">
                A NEW WAY TO EXPLORE AN ANCIENT LANGUAGE
              </div>

              <h1>
                Words that connect.
                <br />
                <span>संस्कृतेन सम्भाषामहे।</span>
              </h1>

              <p className="welcome-description">
                Begin a conversation in Sanskrit. Explore its
                words, discover its beauty, and let curiosity
                lead the way. Every answer comes in Sanskrit
                and English.
              </p>

              <div className="suggestion-heading">
                <span>✦</span> CHOOSE A PLACE TO BEGIN
              </div>

              <div className="suggestions">
                {suggestions.map((item) => (
                  <button
                    className="suggestion-card"
                    key={item.title}
                    onClick={() => sendMessage(item.prompt)}
                  >
                    <span className="suggestion-icon">
                      {item.icon}
                    </span>

                    <span className="suggestion-copy">
                      <strong>{item.title}</strong>
                      <small>{item.subtitle}</small>
                    </span>

                    <span className="suggestion-arrow">
                      ↗
                    </span>
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="messages">
              {messages.map((message, index) => (
                <article
                  className={`message-row ${message.role}`}
                  key={`${index}-${message.role}`}
                >
                  {message.role === "assistant" && (
                    <div className="avatar">सं</div>
                  )}

                  <div className="message-content">
                    <span className="message-author">
                      {message.role === "user"
                        ? "You"
                        : "Samvaad · संवादः"}
                    </span>

                    <div className="message-bubble">
                      {message.role === "assistant"
                        ? renderAnswer(message.content)
                        : message.content}
                    </div>

                    {message.role === "assistant" &&
                      message.suggestions?.length > 0 && (
                        <div className="followup-area">
                          <span className="followup-heading">
                            CONTINUE EXPLORING
                          </span>

                          <div className="followup-list">
                            {message.suggestions
                              .slice(0, 3)
                              .map((question) => (
                                <button
                                  className="followup-chip"
                                  key={question}
                                  disabled={loading}
                                  onClick={() =>
                                    sendMessage(question)
                                  }
                                >
                                  {question}
                                  <span>↗</span>
                                </button>
                              ))}
                          </div>
                        </div>
                      )}
                  </div>

                  {message.role === "user" && (
                    <div className="user-avatar">You</div>
                  )}
                </article>
              ))}

              {loading && (
                <div className="message-row assistant">
                  <div className="avatar">सं</div>

                  <div className="message-content">
                    <span className="message-author">
                      Samvaad · संवादः
                    </span>

                    <div className="message-bubble typing">
                      <span />
                      <span />
                      <span />
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="error-message">
                  <span>{error}</span>
                  <button onClick={retryLastMessage}>
                    Retry
                  </button>
                </div>
              )}

              <div ref={bottomRef} />
            </div>
          )}
        </section>

        <footer className="composer-area">
          <form
            className="composer"
            onSubmit={(event) => {
              event.preventDefault();
              sendMessage();
            }}
          >
            <textarea
              ref={inputRef}
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={(event) => {
                if (
                  event.key === "Enter" &&
                  !event.shiftKey
                ) {
                  event.preventDefault();
                  sendMessage();
                }
              }}
              placeholder="संस्कृतेन लिखतु... Ask me something"
              rows={1}
              maxLength={1000}
              disabled={loading}
              aria-label="Your message"
            />

            <button
              className="send-button"
              type="submit"
              disabled={!input.trim() || loading}
              aria-label="Send message"
            >
              ↗
            </button>
          </form>

          <div className="composer-caption">
            <span>✦</span>
            Every question opens a new door.
            <span className="keyboard-hint">
              ENTER ↵ to send · SHIFT + ENTER for a new line
            </span>
          </div>
        </footer>
      </main>
    </div>
  );
}

export default App;
