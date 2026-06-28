import { useEffect, useState } from "react";

const API_BASE_URL = "http://localhost:8000";

function ChallengeManager(){
    const [challenges, setChallenges] = useState([]);
    const [title, setTitle] = useState("");
    const [description, setDescription] = useState("");
    const [editingId, setEditingId] = useState(null);

    const [error, setError] = useState("");

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

    useEffect(() => {
        fetchChallenges();
    }, []);

    async function handleSubmit(event) {
        event.preventDefault();  // 이벤트 핸들러로 추정
        setError(''); // error 변수 초기화

        const payload = {
            title,
            description,
        }

        try {
            const url = editingId 
            ? `${API_BASE_URL}/api/v1/challenges/${editingId}` 
            : `${API_BASE_URL}/api/v1/challenges`;

            const method = editingId ? "PATCH" : "POST";

            const response = await fetch(url, {
            method: method,
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(payload),
            });

            if (!response.ok){
            throw new Error("챌린지 저장에 실패했습니다.");
            }

            setTitle("");
            setDescription("");
            setEditingId(null);
            fetchChallenges();
        } catch (err) {
            setError(err.message);
        }
    }

    async function handleEdit(challenge) {
        setEditingId(challenge.id);
        setTitle(challenge.title);
        setDescription(challenge.description ?? "");
        }

        async function handleDelete(challengeId){
        const ok = window.confirm("정말 삭제하시겠습니까?");

        if (!ok){
            return;
        }

        try {
            const url = `${API_BASE_URL}/api/v1/challenges/${challengeId}`

            const response = await fetch(url, {
                method: "DELETE",
            });
            
            if (!response.ok) {
            throw new Error("챌린지 삭제에 실패했습니다.")
            }

            fetchChallenges();
        } catch (err) {
            setError(err.message);
        }
    }

    function handleCancelEdit(){
        setEditingId(null);
        setTitle("");
        setDescription("");
    }

    return (
        <section>
            <h2>{editingId ? "챌린지 수정" : "챌린지 생성"}</h2>

            <form onSubmit={handleSubmit}>
            <div>
                <label htmlFor="title">제목</label>
                <input 
                type="text"
                id='title'
                value={title}
                onChange={(event) => setTitle(event.target.value)}
                placeholder="예: 아침 루틴 인증"
                required
                />
            </div>

            <div>
                <label htmlFor="description">설명</label>
                <textarea
                id="description"
                value={description}
                onChange={(event) => setDescription(event.target.value)}
                placeholder="챌린지 설명을 입력하세요."
                />
            </div>
            <button type="submit">
                {editingId ? "수정하기" : "생성하기"}
            </button>
            {editingId && (
                <button type="button" onClick={handleCancelEdit}>
                취소
                </button>
            )}
            </form>
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

                    <button type="button" onClick={() => handleEdit(challenge)}>
                    수정
                    </button>

                    <button type="button" onClick={() => handleDelete(challenge.id)}>
                    삭제
                    </button>
                </li>
                ))}
            </ul>
            )}
            
            {error && <p className="error-message">{error}</p>}
        </section>
    );
}

export default ChallengeManager;