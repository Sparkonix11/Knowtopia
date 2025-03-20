import { useStore } from "vuex";

const store = useStore();

const lectures = computed(() => store.getters["course/getInstructorLectures"]);

