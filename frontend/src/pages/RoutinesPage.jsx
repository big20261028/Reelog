import RoutineManager  from "../components/RoutineManager";

function RoutinePage( {routines, onRoutinesChanged }) {
    return (
        <RoutineManager
            routines={routines}
            onRoutinesChanged={onRoutinesChanged}
        />
    );
}

export default RoutinePage;