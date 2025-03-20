import { ref, computed } from "vue";
import { useStore } from "vuex";
import { createWeekAPI } from "../services/operations/weekAPI";

export function useAddLecture() {
    const store = useStore();  
    const isLoading = ref(false);
    const error = ref(null);

    const creatingCourse = computed(() => store.state.course.creatingCourse);

    const addLecture = async (name) => {
        if (!name) {
            error.value = "Lecture name is required.";
            return;
        }
    
        if (!creatingCourse.value || !creatingCourse.value.id) {
            error.value = "No course found. Please create a course first.";
            return;
        }
    
        isLoading.value = true;
        error.value = null;
    
        try {
            const formData = new FormData();
            formData.append("name", name);
    
            const response = await createWeekAPI(creatingCourse.value.id, formData);
    
            if (!response || response.status !== 201) {
                throw new Error("Failed to add lecture. Please try again.");
            }
    
            // Wait for the Vuex store to update
            await store.dispatch("course/updateInstructorCourses");
    
            // Ensure Vuex updates the current course weeks
            const updatedCourse = store.getters["course/getInstructorCourses"].find(c => c.id === creatingCourse.value.id);
            if (updatedCourse) {
                store.commit("course/SET_CREATING_COURSE_WEEKS", updatedCourse.weeks);
            }
            console.log("Before dispatch:", store.getters["course/getCreatingCourseWeeks"]);
            await store.dispatch("course/updateInstructorCourses");
            console.log("After dispatch:", store.getters["course/getCreatingCourseWeeks"]);

            return response.data;
        } catch (err) {
            error.value = err.message;
        } finally {
            isLoading.value = false;
        }
    };
    
    
    
    return {
        addLecture,
        isLoading,
        error
    };
}
