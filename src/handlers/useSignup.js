import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { useForm } from "../utils/useForm";
import { isNotEmpty, isValidEmail, isValidPhone, passwordsMatch, isStrongPassword } from "../utils/formValidation";

export function useSignup() {
  const router = useRouter();
  const store = useStore();

  // Form validation function
  const validateSignupForm = (formData) => {
    const errors = {};
    
    // Validate first and last name
    if (!isNotEmpty(formData.firstName)) {
      errors.firstName = "First name is required";
    }
    
    if (!isNotEmpty(formData.lastName)) {
      errors.lastName = "Last name is required";
    }
    
    // Validate email
    if (!isNotEmpty(formData.email)) {
      errors.email = "Email is required";
    } else if (!isValidEmail(formData.email)) {
      errors.email = "Please enter a valid email address";
    }
    
    // Validate phone
    if (!isNotEmpty(formData.phoneNumber)) {
      errors.phoneNumber = "Phone number is required";
    } else if (!isValidPhone(formData.countryCode + formData.phoneNumber)) {
      errors.phoneNumber = "Please enter a valid phone number";
    }
    
    // Validate password
    if (!isNotEmpty(formData.password)) {
      errors.password = "Password is required";
    } else if (!isStrongPassword(formData.password)) {
      errors.password = "Password must be at least 8 characters and contain at least one letter and one number";
    }
    
    // Validate confirm password
    if (!isNotEmpty(formData.confirmPassword)) {
      errors.confirmPassword = "Please confirm your password";
    } else if (!passwordsMatch(formData.password, formData.confirmPassword)) {
      errors.confirmPassword = "Passwords do not match";
    }
    
    return {
      isValid: Object.keys(errors).length === 0,
      errors
    };
  };

  // Form submission function
  const submitSignup = async (formData) => {
    // Create FormData for submission
    const submitFormData = new FormData();
    submitFormData.append('is_instructor', formData.selected === "instructor");
    submitFormData.append('fname', formData.firstName);
    submitFormData.append('lname', formData.lastName);
    submitFormData.append('email', formData.email);
    submitFormData.append('phone', formData.countryCode + formData.phoneNumber);
    submitFormData.append('password', formData.password);
    submitFormData.append('password_confirm', formData.confirmPassword);
    
    const response = await store.dispatch("user/signup", submitFormData);
    
    if (response.status === 201) {
      router.push({ name: "Profile" });
      return true;
    } else {
      throw new Error(response.message || "Registration failed. Please try again.");
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
    {
      selected: "student",
      firstName: "",
      lastName: "",
      email: "",
      countryCode: "+91",
      phoneNumber: "",
      password: "",
      confirmPassword: ""
    },
    validateSignupForm,
    submitSignup
  );

  // For backward compatibility
  const selected = computed({
    get: () => formState.value.selected,
    set: (value) => updateField("selected", value)
  });
  const errorMessage = computed(() => submitError.value || "");
  const firstName = computed(() => formState.value.firstName);
  const lastName = computed(() => formState.value.lastName);
  const email = computed(() => formState.value.email);
  const countryCode = computed(() => formState.value.countryCode);
  const phoneNumber = computed(() => formState.value.phoneNumber);
  const password = computed(() => formState.value.password);
  const confirmPassword = computed(() => formState.value.confirmPassword);
  
  // Computed properties
  const is_instructor = computed(() => selected.value === "instructor");
  const fullPhoneNumber = computed(() => countryCode.value + phoneNumber.value);
  const user = computed(() => store.getters["user/currentUser"]);

  // For backward compatibility
  const updateFirstName = (event) => {
    updateField("firstName", event.target.value);
  };
  
  const updateLastName = (event) => {
    updateField("lastName", event.target.value);
  };
  
  const updateEmail = (event) => {
    updateField("email", event.target.value);
  };
  
  const updateCountryCode = (event) => {
    updateField("countryCode", event.target.value);
  };
  
  const updatePhoneNumber = (event) => {
    updateField("phoneNumber", event.target.value);
  };
  
  const updatePassword = (event) => {
    updateField("password", event.target.value);
  };
  
  const updateConfirmPassword = (event) => {
    updateField("confirmPassword", event.target.value);
  };

  // Signup operation handler (for backward compatibility)
  const signup = async () => {
    return await submitForm();
  };

  return {
    // State
    selected,
    errorMessage,
    firstName,
    lastName,
    email,
    countryCode,
    phoneNumber,
    password,
    confirmPassword,
    errors,
    isSubmitting,
    
    // Computed
    is_instructor,
    
    // Methods
    updateFirstName,
    updateLastName,
    updateEmail,
    updateCountryCode, 
    updatePhoneNumber,
    updatePassword,
    updateConfirmPassword,
    signup,
    
    // New form methods
    handleInput,
    updateField
  };
}