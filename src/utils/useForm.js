import { ref, reactive } from 'vue';

/**
 * A composable for handling form state, validation, and submission
 * 
 * @param {Object} initialState - The initial state of the form
 * @param {Function} validateFn - A function that validates the form data and returns validation results
 * @param {Function} submitFn - A function that handles form submission
 * @returns {Object} Form state and methods
 */
export function useForm(initialState, validateFn, submitFn) {
  // Form state
  const formState = ref({ ...initialState });
  const errors = ref({});
  const isSubmitting = ref(false);
  const submitError = ref('');
  const isValid = ref(false);

  /**
   * Updates a specific field in the form state
   * 
   * @param {string} field - The field name to update
   * @param {any} value - The new value for the field
   */
  const updateField = (field, value) => {
    formState.value[field] = value;
    
    // Clear error for this field when it's updated
    if (errors.value[field]) {
      const newErrors = { ...errors.value };
      delete newErrors[field];
      errors.value = newErrors;
    }
    
    // Clear general submit error when any field is updated
    if (submitError.value) {
      submitError.value = '';
    }
  };

  /**
   * Generic input handler for v-model or @input events
   * 
   * @param {string} field - The field name to update
   * @param {Event|any} event - The input event or direct value
   */
  const handleInput = (field, event) => {
    // Handle both direct values and event objects
    const value = event && event.target ? event.target.value : event;
    updateField(field, value);
  };

  /**
   * Validates the form without submitting
   * 
   * @returns {boolean} Whether the form is valid
   */
  const validateForm = () => {
    const validationResult = validateFn(formState.value);
    errors.value = validationResult.errors || {};
    isValid.value = validationResult.isValid;
    return isValid.value;
  };

  /**
   * Submits the form if it's valid
   * 
   * @returns {Promise<boolean>} Whether the submission was successful
   */
  const submitForm = async () => {
    // Reset errors
    errors.value = {};
    submitError.value = '';
    
    // Validate form
    const isFormValid = validateForm();
    if (!isFormValid) {
      return false;
    }
    
    // Submit form
    isSubmitting.value = true;
    try {
      await submitFn(formState.value);
      return true;
    } catch (error) {
      submitError.value = error.message || 'An error occurred during submission';
      return false;
    } finally {
      isSubmitting.value = false;
    }
  };

  /**
   * Resets the form to its initial state
   */
  const resetForm = () => {
    formState.value = { ...initialState };
    errors.value = {};
    submitError.value = '';
    isValid.value = false;
  };

  return {
    formState,
    errors,
    isSubmitting,
    submitError,
    isValid,
    updateField,
    handleInput,
    validateForm,
    submitForm,
    resetForm
  };
}