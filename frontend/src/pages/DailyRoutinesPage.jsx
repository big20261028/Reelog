import DailyRoutineManager from "../components/DailyRoutineManager";

function DailyRoutinesPage( {routines, onRoutinesChanged }) {
    return (
        <DailyRoutineManager
            routines={routines}
            onRoutinesChanged={onRoutinesChanged}
        />
    );
}

export default DailyRoutinesPage;