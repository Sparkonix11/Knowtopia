import { ref, computed } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

export function useSignup() {
  const router = useRouter();
  const store = useStore();

  // Form state
  const selected = ref("student");
  const errorMessage = ref("");
  const firstName = ref("");
  const lastName = ref("");
  const email = ref("");
  const countryCode = ref("+91");
  const phoneNumber = ref("");
  const password = ref("");
  const confirmPassword = ref("");

  // Computed properties
  const is_instructor = computed(() => selected.value === "instructor");
  const fullPhoneNumber = computed(() => countryCode.value + phoneNumber.value);
  const user = computed(() => store.getters["user/currentUser"]);

  // Form update handlers
  const updateFirstName = (event) => {
    firstName.value = event.target.value;
  };
  
  const updateLastName = (event) => {
    lastName.value = event.target.value;
  };
  
  const updateEmail = (event) => {
    email.value = event.target.value;
  };
  
  const updateCountryCode = (event) => {
    countryCode.value = event.target.value;
  };
  
  const updatePhoneNumber = (event) => {
    phoneNumber.value = event.target.value;
  };
  
  const updatePassword = (event) => {
    password.value = event.target.value;
  };
  
  const updateConfirmPassword = (event) => {
    confirmPassword.value = event.target.value;
  };

  // Form validation
  const validateForm = () => {
    errorMessage.value = "";
    
    if (!firstName.value.trim() || !lastName.value.trim()) {
      errorMessage.value = "Please enter both first and last name.";
      return false;
    }
    
    if (!email.value.trim()) {
      errorMessage.value = "Please enter your email address.";
      return false;
    }
    
    if (!phoneNumber.value.trim()) {
      errorMessage.value = "Please enter your phone number.";
      return false;
    }
    
    if (!password.value.trim() || !confirmPassword.value.trim()) {
      errorMessage.value = "Please enter both password fields.";
      return false;
    }
    
    if (password.value !== confirmPassword.value) {
      errorMessage.value = "Passwords do not match.";
      return false;
    }
    
    return true;
  };

  // Signup operation handler
  const signup = async () => {
    if (!validateForm()) {
      return;
    }
    
    // Create FormData for submission
    const formData = new FormData();
    formData.append('is_instructor', is_instructor.value);
    formData.append('fname', firstName.value);
    formData.append('lname', lastName.value);
    formData.append('email', email.value);
    formData.append('phone', fullPhoneNumber.value);
    formData.append('password', password.value);
    formData.append('password_confirm', confirmPassword.value);
    
    try {
      const response = await store.dispatch("user/signup", formData);
      
      if (response.status === 201) {
        router.push({ name: "Profile" });
        return true;
      } else {
        errorMessage.value = response.message || "Registration failed. Please try again.";
        return false;
      }
    } catch (error) {
      errorMessage.value = error.message || "Registration failed. Please try again.";
      return false;
    }
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
    signup
  };
}