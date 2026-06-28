import { Link, Route, Routes } from "react-router-dom";
import { useEffect, useState } from "react";
import "./App.css"

import HomePage from "./pages/HomePage";
import RoutinePage from "./pages/RoutinesPage";
import DailyRoutinesPage from "./pages/DailyRoutinesPage";
import ChallengePage from "./pages/ChallengesPage";

// import RoutineManager from "./components/RoutineManager";
// import DailyRoutineManager from "./components/DailyRoutineManager";

const API_BASE_URL = "http://localhost:8000";

function App() {
  // const [health, setHealth] = useState(null);

  // const [challenges, setChallenges] = useState([]);
  // const [title, setTitle] = useState("");
  // const [description, setDescription] = useState("");
  // const [editingId, setEditingId] = useState(null);
  
  const [routines, setRoutines] = useState([]);
  const [error, setError] = useState("");

  // async function fetchHealth() {
  //   try {
  //     const response = await fetch(`${API_BASE_URL}/api/v1/health`);

  //     if (!response.ok) {
  //       throw new Error("서버 응답이 정상적이지 않습니다.");
  //     }

  //     const data = await response.json();
  //     setHealth(data);
  //   } catch (err) {
  //     setError(err.message);
  //   }
  // }

  async function fetchRoutines() {
      try{
          const response = await fetch(`${API_BASE_URL}/api/v1/routines`);

          if (!response.ok){
              throw new Error("루틴 템플릿 목록을 불러오지 못했습니다.");
          }

          const data = await response.json();
          setRoutines(data);
      }catch (err){
          setError(err.message);
      }
  }

  useEffect(() => {
    // fetchHealth();
    fetchRoutines();
  }, []);

  

  return (
    <main>
      <header>
        <h1>Reelog</h1>
        <p>루틴 인증 기반 숏폼 기록 서비스</p>

        {/* <section>
          <h2>서버 연결 상태</h2> */}
          {/* 삼항연산자 사용 */}
          {/* {health ? (
            <pre>{JSON.stringify(health, null, 2)}</pre>
          ) : (
            <p>서버 상태를 확인하는 중입니다.</p>
          )}
        </section> */}

        <nav className="app-nav">
            <Link to="/">홈</Link>
            <Link to="/routines">루틴 템플릿</Link>
            <Link to="/daily">오늘의 루틴</Link>
            <Link to="/challenges">챌린지</Link>
        </nav>
      </header>

      {error && <p className="error-message">{error}</p>}

      <Routes>
        <Route path="/" element={<HomePage />} />
        
        <Route 
            path="/routines"
            element={
              <RoutinePage 
                routines={routines}
                onRoutinesChanged={fetchRoutines}
              />
            }
          />
        
        <Route
           path="/daily"
            element={
              <DailyRoutinesPage 
                routines={routines}
                onRoutinesChanged={fetchRoutines}
              />
            }
        />

        <Route path="/challenges" element={<ChallengePage />} />
      </Routes>
    </main>
  );
}

export default App;