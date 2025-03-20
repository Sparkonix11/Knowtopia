import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export function useLogin() {
  const router = useRouter();
  const store = useStore();

  // Form state
  const selected = ref("student");
  const errorMessage = ref("");
  const email = ref("");
  const password = ref("");

  // Computed properties
  const user = computed(() => store.getters["user/currentUser"]);

  // Form update handlers
  const updateEmail = (event) => {
    email.value = event.target.value;
  };
  
  const updatePassword = (event) => {
    password.value = event.target.value;
  };

  // Validation
  const validateForm = () => {
    errorMessage.value = "";
    if (!email.value.trim() || !password.value.trim()) {
      errorMessage.value = "Please enter both email and password.";
      return false;
    }
    return true;
  };

  // Login operation handler
  const login = async () => {
    if (!validateForm()) {
      return false;
    }

    const formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);

    try {
      const response = await store.dispatch("user/login", formData);

      if (response.status === 200) {
        // Redirect based on user type
        if (!user.value?.is_instructor) {
          router.push({ name: "StudentDashboard" });
        } else {
          router.push({ name: "InstructorDashboard" });
        }
        return true;
      } else {
        errorMessage.value = response.message || "Login failed. Please try again.";
        return false;
      }
    } catch (error) {
      errorMessage.value = error.message || "Login failed. Please try again.";
      return false;
    }
  };

  return {
    // State
    selected,
    errorMessage,
    email,
    password,
    
    // Computed
    user,
    
    // Methods
    updateEmail,
    updatePassword,
    login
  };
}