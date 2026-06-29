import { useEffect, useState } from "react";

import ProofManager from "./ProofManager";

const API_BASE_URL = "http://localhost:8000";

function DailyRoutineManager({ routines, onRoutinesChanged }){
    // const [routines, setRoutines] = useState([]);
    const [dailyRoutines, setDailyRoutines] = useState([]);
    const [selectedRoutineId, setSelectedRoutineId] = useState("");
    const [error, setError] = useState("");

    // async function fetchRoutines() {
    //     try{
    //         const response = await fetch(`${API_BASE_URL}/api/v1/routines`);

    //         if (!response.ok){
    //             throw new Error("루틴 템플릿 목록을 불러오지 못했습니다.");
    //         }

    //         const data = await response.json();
    //         setRoutines(data);
    //     }catch (err){
    //         setError(err.message);
    //     }
    // }

    async function fetchTodayDailyRoutines(){
        try{
            const response = await fetch(`${API_BASE_URL}/api/v1/daily-routines/today`);

            if(!response.ok){
                throw new Error("오늘의 루틴 목록을 불러오지 못했습니다.");
            }

            const data = await response.json();
            setDailyRoutines(data);
        }catch(err){
            setError(err.message);
        }
    }
    useEffect(() => { // 페이지 로딩 시 바로 실행시키는듯?
        // fetchRoutines();


        fetchTodayDailyRoutines();
    }, []);

    useEffect(() => { // 삭제된 루틴을 선택해둔 상태라면 초기화해버리기
        if (!selectedRoutineId) {
            return;
        }

        const exists = routines.some(
            (routine) => String(routine.id) === String(selectedRoutineId)
        );

        if (!exists) {
            setSelectedRoutineId("");
        }
    }, [routines, selectedRoutineId]);

    async function handleCreateDailyRoutine(event){
        event.preventDefault();
        setError("");

        if (!selectedRoutineId){
            setError("루틴 템플릿을 먼저 선택하세요.");
            return;
        }

        const selectedRoutine = routines.find(
            (routine) => String(routine.id) === String(selectedRoutineId)
        );

        if (!selectedRoutine) {
            setError("선택한 루틴 템플릿이 삭제되었거나 최신 목록에 없습니다.");
            setSelectedRoutineId("");
            return;
        }

        try {
            const response = await fetch(
                `${API_BASE_URL}/api/v1/daily-routines/from-routine/${selectedRoutineId}`,
                {
                    method : "POST",
                }
            );
            
            if (!response.ok){
                if (response.status == 409){
                    throw new Error("이미 오늘 생성된 데일리 루틴입니다.");
                }
                if (response.status === 404){
                    throw new Error("선택한 루틴 템플릿을 찾을 수 없습니다.");
                }

                throw new Error("오늘의 루틴 생성에 실패했습니다.");
            }

            setSelectedRoutineId("");
            await fetchTodayDailyRoutines();
            await onRoutinesChanged();
        }catch(err){
            setError(err.message);
        }
    }

    async function handleCompleteItem(itemId){
        setError("");

        try {
            const response = await fetch(
                `${API_BASE_URL}/api/v1/daily-routine-items/${itemId}/complete`,
                {
                    method: "PATCH",
                }
            );

            if (!response.ok) {
                throw new Error("루틴 항목 완료 처리에 실패했습니다.");
            }

            fetchTodayDailyRoutines();
        }catch (err){
            setError(err.message);
        }
    }

    async function handleCancelItem(itemId){
        setError("");

        try {
            const response = await fetch(
                `${API_BASE_URL}/api/v1/daily-routine-items/${itemId}/cancel`,
                {
                    method : "PATCH",
                }
            );

            if(!response.ok){
                const errorData = await response.json().catch(() => null)

                throw new Error(
                    errorData?.detail ?? "루틴 항목 완료 취소에 실패했습니다."
                );
            }

            fetchTodayDailyRoutines();
        }catch (err){
            setError(err.message);
        }
    }

    function getCompletedCount(items){
        return items.filter((item) => item.is_completed).length;
    }

    function getStatusLabel(status){
        if (status === "PENDING"){
            return "대기";
        }

        if (status === "IN_PROGRESS"){
            return "진행 중";
        }
        
        if (status === "COMPLETED"){
            return "완료";
        }

        return status;
    }

    return (
        <section>
            <h2>오늘의 루틴</h2>
            <p>
                루틴 템플릿을 선택해 오늘 수행할 루틴 기록을 생성하고, 항목별 완료 상태를 관리합니다.
            </p>

            <form onSubmit={handleCreateDailyRoutine} className="sub-form">
                <h3>오늘 루틴 생성</h3>

                <div>
                    <label htmlFor="daily-routine-select">루틴 템플릿 선택</label>
                    <select 
                        name="daily-routine-select" 
                        id="daily-routine-select"
                        value={selectedRoutineId}
                        onChange={(event) => setSelectedRoutineId(event.target.value)}
                    >
                        <option value="">루틴 템플릿을 선택하세요.</option>

                        {routines.map((routine) => (
                            <option key={routine.id} value={routine.id}>
                                {routine.title}
                            </option>
                        ))}
                    </select>
                </div>

                <button type="submit">오늘 루틴 생성</button>
            </form>

            <div className="daily-routine-list">
                {dailyRoutines.length === 0 ? (
                    <p>오늘 생성된 루틴이 없습니다.</p>
                ) : (
                    dailyRoutines.map((dailyRoutine) => {
                        const items = dailyRoutine.items ?? [];
                        const completedCount = getCompletedCount(items);

                        return (
                            <article key={dailyRoutine.id} className="daily-routine-card">
                                <div className="routine-card-header">
                                    <div>
                                        <strong>{dailyRoutine.title}</strong>
                                        <p>{dailyRoutine.description || "설명이 없습니다."}</p>
                                        <p className="daily-routine-meta">
                                            날짜 : {dailyRoutine.target_date} / 상태:{" "} 
                                            {getStatusLabel(dailyRoutine.status)} / 완료율:{" "}
                                            {completedCount} / {items.length}
                                        </p>
                                    </div>
                                </div>

                                <div>
                                    <h3>오늘 수행 항목</h3>

                                    {items.length === 0 ? (
                                        <p>등록된 항목이 없습니다.</p>
                                    ) : (
                                        <ul>
                                            {items.map((item) => (
                                                <li
                                                    key={item.id}
                                                    className={item.is_completed ? "completed-item" : ""}
                                                >
                                                    <strong>
                                                        {item.sequence}. {item.title}
                                                    </strong>
                                                    <p>{item.description || "설명이 없습니다."}</p>

                                                    <p>
                                                        상태:{" "}
                                                        {item.is_completed ? "완료" : "미완료"}
                                                    </p>

                                                    <p>
                                                        인증 자료 : {item.proof_count ?? 0}개
                                                    </p>

                                                    {item.completed_at && (
                                                        <p>완료 시간: {item.completed_at}</p>
                                                    )}

                                                    {item.is_completed ? (
                                                        <>
                                                            <button 
                                                                type="button" 
                                                                onClick={() => handleCancelItem(item.id)}
                                                                disabled={(item.proof_count ?? 0) > 0}
                                                            >
                                                                완료 취소
                                                            </button>

                                                            {(item.proof_count ?? 0) > 0 && (
                                                                <p className="routine-policy-message">
                                                                    인증 파일이 있는 항목은 인증 삭제를 통해 미완료로 변경할 수  있습니다.
                                                                </p>
                                                            )}
                                                        </>
                                                    ) : (
                                                        <button type="button" onClick={() => handleCompleteItem(item.id)}>
                                                            완료 처리
                                                        </button>
                                                    )}

                                                    <ProofManager 
                                                        itemId={item.id}
                                                        onProofsChanged={fetchTodayDailyRoutines}
                                                    />
                                                </li>
                                            ))}
                                        </ul>
                                    )}
                                </div>
                            </article>
                        );
                    })
                )}
            </div>

            {error && <p className="error-message">{error}</p>}
        </section>
    );
}

export default DailyRoutineManager;