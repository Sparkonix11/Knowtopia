import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useForm } from "../utils/useForm";
import { isNotEmpty, isValidEmail, createValidationResult } from "../utils/formValidation";

export function useLogin() {
  const router = useRouter();
  const store = useStore();

  // Form validation function
  const validateLoginForm = (formData) => {
    const errors = {};
    
    if (!isNotEmpty(formData.email)) {
      errors.email = "Email is required";
    } else if (!isValidEmail(formData.email)) {
      errors.email = "Please enter a valid email address";
    }
    
    if (!isNotEmpty(formData.password)) {
      errors.password = "Password is required";
    }
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };

  // Form submission function
  const submitLogin = async (formData) => {
    const submitFormData = new FormData();
    submitFormData.append('email', formData.email);
    submitFormData.append('password', formData.password);

    const response = await store.dispatch("user/login", submitFormData);

    if (response.status === 200) {
      // Redirect based on user type
      if (!user.value?.is_instructor) {
        router.push({ name: "StudentDashboard" });
      } else {
        router.push({ name: "InstructorDashboard" });
      }
      return true;
    } else {
      throw new Error(response.message || "Login failed. Please try again.");
    }
  };

  // Initialize form with useForm composable
  const {
    formState,
    errors,
    isSubmitting,
    submitError,
    updateField,
    handleInput,
    submitForm
  } = useForm(
    { email: "", password: "" },
    validateLoginForm,
    submitLogin
  );

  // For backward compatibility
  const selected = ref("student");
  const errorMessage = computed(() => submitError.value || "");
  const email = computed(() => formState.value.email);
  const password = computed(() => formState.value.password);
  
  // Computed properties
  const user = computed(() => store.getters["user/currentUser"]);

  // For backward compatibility
  const updateEmail = (event) => {
    updateField("email", event.target.value);
  };
  
  const updatePassword = (event) => {
    updateField("password", event.target.value);
  };

  // Login operation handler (for backward compatibility)
  const login = async () => {
    return await submitForm();
  };

  return {
    // State
    selected,
    errorMessage,
    email,
    password,
    errors,
    isSubmitting,
    
    // Computed
    user,
    
    // Methods
    updateEmail,
    updatePassword,
    login,
    
    // New form methods
    handleInput,
    updateField
  };
}