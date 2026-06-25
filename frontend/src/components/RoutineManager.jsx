import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

function RoutineManager(){
  const [routines, setRoutines] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [editingId, setEditingId] = useState(null);

  const [itemTitle, setItemTitle] = useState("");
  const [itemDescription, setItemDescription] = useState("");
  const [selectedRoutineId, setSelectedRoutineId] = useState("");

  const [error, setError] = useState("");

  async function fetchRoutines() {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/routines`);

      if (!response.ok){
        throw new Error("루틴 목록을 불러오지 못했습니다.");
      }

      const data = await response.json();
      setRoutines(data);
    } catch (err) {
      setError(err.message);
    }
  }

  useEffect(() => {
    fetchRoutines();
  }, []);

  async function handleSubmit(event){
    event.preventDefault();
    setError("");

    const payload = {
      title,
      description,
      items: [],
    };

    try{
      const url = editingId
        ? `${API_BASE_URL}/api/v1/routines/${editingId}`
        : `${API_BASE_URL}/api/v1/routines`;
      
      const method = editingId ? "PATCH" : "POST";

      const response = await fetch(url, {
        method: method,
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok){
        throw new Error("루틴 저장에 실패했습니다.");
      }

      setTitle("");
      setDescription("");
      setEditingId(null);

      fetchRoutines(); // 루틴 목록 다시 받아와서 갱신하기
    } catch (err){
      setError(err.message);
    }
  }

  function handleEdit(routine){
    setEditingId(routine.id);
    setTitle(routine.title);
    setDescription(routine.description ?? "");
  }

  function handleCancelEdit(){
    setEditingId(null);
    setTitle("");
    setDescription("");
  }

  async function handleDeleteRoutine(routineId){
    const ok = window.confirm("루틴을 삭제하시겠습니까? 루틴 항목도 함께 삭제됩니다.");

    if (!ok){
      return;
    }

    try{
      const response = await fetch(`${API_BASE_URL}/api/v1/routines/${routineId}`, {
        method:"DELETE",
      });

      if (!response.ok){
        throw new Error("루틴 삭제에 실패했습니다.");
      }

      fetchRoutines();
    }catch(err){
      setError(err.message);
    }
  }

  async function handleAddItem(event){
    event.preventDefault();
    setError("");

    if (!selectedRoutineId){
      setError("루틴을 먼저 입력하세요.");
      return;
    }

    const payload = {
      title: itemTitle,
      description: itemDescription,
      sequence: 1,
    }

    try{
      const response = await fetch(
        `${API_BASE_URL}/api/v1/routines/${selectedRoutineId}/items`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(payload)
        }
      );

      if (!response.ok){
        throw new Error("루틴 항목 추가에 실패했습니다.");
      }

      setItemTitle("");
      setItemDescription("");

      fetchRoutines();
    }catch(err){
      setError(err.message);
    }
  }

  async function handleDeleteItem(routineId, itemId){
    const ok = window.confirm("루틴 항목을 삭제하시겠습니까?");

    if (!ok){
      return;
    }

    try{
      const response = await fetch(
        `${API_BASE_URL}/api/v1/routines/${routineId}/items/${itemId}`,
        {
          method:"DELETE",
        }
      );
      
      if (!response.ok){
        throw new Error("루틴 항목 삭제에 실패했습니다.");
      }

      fetchRoutines();
    } catch(err){
      setError(err.message);
    }
  }

  return (
    <section>
      <h2>루틴 템플릿 관리</h2>
      <p>
        반복해서 사용할 루틴 템플릿을 만들고, 각 루틴에 수행 항목을 추가합니다.
      </p>

      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="routine-title">루틴 제목</label>
          <input 
            type="text" 
            id="routine-title" 
            value={title} 
            onChange={(event)=>setTitle(event.target.value)}
            placeholder="예: 취준 루틴"
            required
          />
        </div>

        <div>
          <label htmlFor="routine-description">루틴 설명</label>
          <textarea 
            id="routine-description" 
            value={description} 
            onChange={(event)=>setDescription(event.target.value)}
            placeholder="예: 매일 취업 준비를 기록하는 루틴"
          />
        </div>

        <button type="submit">
          {editingId ? "루틴 수정" : "루틴 생성"}
        </button>

        {editingId && (
          <button type="button" onClick={handleCancelEdit}>
            취소
          </button>
        )}
      </form>

      <form onSubmit={handleAddItem} className="sub-form">
        <h3>루틴 항목 추가</h3>

        <div>
          <label htmlFor="routine-select">루틴 선택</label>
          <select 
            name="routine-select" 
            id="routine-select"
            value={selectedRoutineId}
            onChange={(event)=> setSelectedRoutineId(event.target.value)}
          >
            <option value="">루틴을 선택하세요</option>
            {routines.map((routine) => (
              <option key={routine.id} value={routine.id}>
                {routine.title}
              </option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="item-title">항목 제목</label>
          <input 
            type="text" 
            id="item-title"
            value={itemTitle}
            onChange={(event) => setItemTitle(event.target.value)}
            placeholder="예: 알고리즘 1문제"
            required
          />
        </div>

        <div>
          <label htmlFor="item-description">항목 설명</label>
          <textarea
            id="item-description"
            value={itemDescription}
            onChange={(event) => setItemDescription(event.target.value)}
            placeholder="예: 백준 또는 프로그래머스 문제 풀이"
          />
        </div>

        <button type="submit">항목 추가</button>
      </form>

      <div className="routine-list">
        {routines.length === 0 ? (
          <p>아직 등록된 루틴이 없습니다.</p>
        ) : (
          routines.map((routine) => (
            <article key={routine.id} className="routine-card">
              <div className="routine-card-header">
                <div>
                  <strong>{routine.title}</strong>
                  <p>{routine.description}</p>
                </div>

                <div>
                  <button type="button" onClick={() => handleEdit(routine)}>
                    수정
                  </button>
                  <button 
                    type="button"
                    onClick={() => handleDeleteRoutine(routine.id)}
                  >
                    삭제
                  </button>
                </div>
              </div>

              <div>
                <h3>루틴 항목</h3>

                {routine.items.length === 0 ? (
                  <p>등록된 항목이 없습니다.</p>
                ) : (
                  <ul>
                    {routine.items.map((item) => (
                      <li key={item.id}>
                        <strong>
                          {item.sequence}. {item.title}
                        </strong>
                        <p>{item.description}</p>

                        <button type="button" onClick={() => handleDeleteItem(routine.id, item.id)}>
                          항목 삭제
                        </button>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            </article>
          ))
        )}
      </div>

      {error && <p className="error-message">{error}</p>}
    </section>
  );
}

export default RoutineManager;