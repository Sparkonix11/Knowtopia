import { ref, computed, watchEffect } from "vue";
import { useStore } from "vuex";

export function useCreateLectures() {
    const store = useStore();

    const creatingCourse = computed(() => store.getters["course/getCreatingCourse"]);
    const creatingCourseWeeks = computed(() => store.getters["course/getCreatingCourseWeeks"]);

    // Function to fetch updated weeks when needed
    const updateWeeks = async () => {
        if (!creatingCourse.value) return;
        await store.dispatch("course/updateInstructorCourses"); // Fetch latest data
    };

    

    return {
        creatingCourse,
        creatingCourseWeeks,
        updateWeeks
    };
}