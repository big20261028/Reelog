import { useEffect, useState } from "react";
import "./App.css"

const API_BASE_URL = "http://localhost:8000";

function App() {
  const [health, setHealth] = useState(null);
  const [challenges, setChallenges] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchHealth() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/health`);
        if (!response.ok) {
          throw new Error("서버 응답이 정상적이지 않습니다.");
        }
        const data = await response.json();
        setHealth(data);
      } catch (err) {
        setError(err.message);
      }
    }

    async function fetchChallenges() {
      try {
        const response = await fetch(`${API_BASE_URL}/api/v1/challenges`);
        if (!response.ok) {
          throw new Error("챌린지 목록을 불러오지 못했습니다.");
        }
        const data = await response.json();
        setChallenges(data);
      } catch (err) {
        setError(err.message);
      }
    }

    fetchHealth();
    fetchChallenges();

  }, []);

  return (
    <main style={{ maxWidth: "720px", margin: "40px auto", padding: "0 20px" }}>
      <h1>Reelog</h1>
      <p>루틴 인증 기반 숏폼 기록 서비스</p>

      <section>
        <h2>서버 연결 상태</h2>
        {/* 삼항연산자 사용 */}
        {health ? (
          <pre>{JSON.stringify(health, null, 2)}</pre>
        ) : (
          <p>서버 상태를 확인하는 중입니다.</p>
        )}
      </section>
      
      <section>
        <h2>챌린지 목록</h2>
        {challenges.length === 0 ? (
          <p>챌린지가 없습니다.</p>
        ) : (
          <ul>
            {/* 화살표 함수 다음 결과를 바로 리턴하려면 일반 괄호를 써도 된다. */}
            {challenges.map((challenge) => (
              <li key={challenge.id}>
                <strong>{challenge.title}</strong>
                <p>{challenge.description}</p>
              </li>
            ))}
          </ul>
        )}
      </section>

      {error && (
        <section>
          <h2>에러</h2>
          <p style={{color: "red"}}>{error}</p>
        </section>
      )}
    </main>
  );
}

export default App;