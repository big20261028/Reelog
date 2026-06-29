import { useEffect, useState } from "react";
import { API_BASE_URL } from "../constants/api";

function ProofManager({ itemId, onProofsChanged } ){
    const [proofs, setProofs] = useState([]);
    const [file, setFile] = useState(null);
    const [note, setNote] = useState("");
    const [error, setError] = useState("");
    const [isUploading, setIsUploading] = useState(false);

    // 최대 업로드 파일 개수
    const MAX_PROOFS_PER_ITEM = 5;

    // action 때마다 재설정 되도록 밖에다 선언
    const proofCount = proofs.length;
    const isMaxProofCount = proofCount >= MAX_PROOFS_PER_ITEM;

    async function fetchProofs() {
        try{
            const response = await fetch(
                `${API_BASE_URL}/api/v1/daily-routine-items/${itemId}/proofs`
            );

            if (!response.ok){
                throw new Error("인증 목록을 불러오지 못했습니다.");
            }

            const data = await response.json();
            setProofs(data);
        } catch (err){
            setError(err.message);
        }
    }

    useEffect(() => {
        fetchProofs();
    }, [itemId]); //itemId 값이 바뀔때마다 재실행됨

    async function handleUpload(event){
        event.preventDefault();
        setError("");

        if(!file){
            setError("업로드할 파일을 선택하세요.");
            return;
        }

        const formData = new FormData();  // 텍스트가 아닌 파일을 받기 위해 FormData 사용
        formData.append("file", file);
        formData.append("note", note);

        try {
            setIsUploading(true);

            const response = await fetch(
                `${API_BASE_URL}/api/v1/daily-routine-items/${itemId}/proofs`,
                {
                    method: "POST",
                    body: formData,
                }
            );

            if (!response.ok){
                const errorData = await response.json().catch(() => null)

                throw new Error(
                    errorData?.detail ?? "인증 파일 업로드에 실패했습니다."
                );
            }

            setFile(null);
            setNote("");

            const fileInput = document.getElementById(`proof-file-${itemId}`);
            if (fileInput){
                fileInput.value = "";
            }

            await fetchProofs();

            if (onProofsChanged){
                await onProofsChanged();
            }
        } catch(err){
            setError(err.message);
        } finally {
            setIsUploading(false);
        }
    }

    async function handleDeleteProof(proofId){
        const ok = window.confirm("인증 기록을 삭제하시겠습니까?");

        if (!ok){
            return;
        }

        try {
            const response = await fetch(
                `${API_BASE_URL}/api/v1/proofs/${proofId}`,
                {method: "DELETE",},
            );

            if (!response.ok){
                throw new Error("인증 기록 삭제에 실패했습니다.");
            }

            await fetchProofs();
            if (onProofsChanged){
                await onProofsChanged();
            }
        } catch(err){
            setError(err.message);
        }
    }

    function getFileUrl(fileUrl){
        return `${API_BASE_URL}${fileUrl}`;
    }




    return (
        <div className="proof-manager">
            <h4>인증 파일</h4>

            <p>
                인증 자료: {proofCount} / {MAX_PROOFS_PER_ITEM}
            </p>
            {isMaxProofCount && (
                <p className="error-message">
                    인증 파일은 최대 {MAX_PROOFS_PER_ITEM}개까지만 등록할 수 있습니다.
                </p>
            )}

            <form onSubmit={handleUpload} className="proof-upload-form">
                <div>
                    <label htmlFor={`proof-file-${itemId}`}>파일 선택</label>
                    <input 
                        type="file"
                        id={`proof-file-${itemId}`}
                        accept="image/jpeg,image/png,image/webp,video/mp4,video/quicktime"
                        disabled={isMaxProofCount ? true : false}
                        onChange={(event) => setFile(event.target.files[0] ?? null)}
                    />
                </div>

                <div>
                    <label htmlFor={`proof-note-${itemId}`}>인증 메모</label>
                    <input 
                        type="text"
                        id={`proof-note-${itemId}`}
                        value={note}
                        disabled={isMaxProofCount ? true : false}
                        onChange={(event) => setNote(event.target.value)}
                        placeholder="예: 알고리즘 풀이 완료"
                    />
                </div>

                <button type="submit" disabled={isUploading || isMaxProofCount}>
                    {
                        isMaxProofCount ? ("업로드 불가") : (isUploading ? "업로드 중..." : "인증 업로드")
                    }
                </button>
            </form>

            {proofs.length === 0 ? (
                <p>등록된 인증 파일이 없습니다.</p>
            ) : (
                <ul className="proof-list">
                    {proofs.map((proof, index) => {
                        const media = proof.media_asset;
                        const fileUrl = getFileUrl(media.file_url);
                        const isImage = media.content_type.startsWith("image/");
                        const isVideo = media.content_type.startsWith("video/");

                        return (
                            <li key={proof.id} className="proof-item">
                                <p>
                                    <strong>파일명:</strong> {media.original_filename}
                                </p>
                                
                                {proof.note && (
                                    <p>
                                        <strong>메모:</strong> {proof.note}
                                    </p>
                                )}

                                {isImage && (
                                    <img
                                        src={fileUrl}
                                        alt={media.original_filename}
                                        className="proof-preview-image"
                                    />
                                )}

                                {isVideo && (
                                    <video
                                        src={fileUrl}
                                        controls
                                        className="proof-preview-video"
                                    />
                                )}
                                
                                <div>
                                    <a href={fileUrl} target="_blank" rel="noreferrer">
                                        파일 열기
                                    </a>
                                    <button
                                        type="button"
                                        onClick={() => handleDeleteProof(proof.id)}
                                    >
                                        인증 삭제
                                    </button>
                                </div>
                            </li>
                        );
                    })}
                </ul>
            )}

            {error && <p className="error-message">{error}</p>}
            
        </div>
    );
}

export default ProofManager;