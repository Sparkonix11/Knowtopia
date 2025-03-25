import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { submitReviewAPI } from '../services/operations/reviewAPI';
import { isNotEmpty, createValidationResult } from '../utils/formValidation';
import { useForm } from '../utils/useForm';

export function useWriteReview(materialId, onSuccess) {
  const store = useStore();
  const user = computed(() => store.getters["user/currentUser"]);
  
  // Form state initialization
  const initialState = {
    rating: 0,
    comment: ''
  };
  
  // Additional UI state
  const hoverRating = ref(0);
  const success = ref(false);
  
  // Form validation function
  const validateReviewForm = (formData) => {
    const errors = {};
    
    if (formData.rating === 0) {
      errors.rating = 'Please select a rating';
    }
    
    if (!isNotEmpty(formData.comment)) {
      errors.comment = 'Please write a review';
    }
    
    return createValidationResult(Object.keys(errors).length === 0, errors);
  };
  
  // Form submission function
  const submitReview = async (formData) => {
    try {
      const payload = {
        materialId: materialId,
        rating: formData.rating,
        comment: formData.comment.trim()
      };
      
      const response = await submitReviewAPI(payload);
      
      if (response.status === 200 || response.status === 201) {
        success.value = true;
        setTimeout(() => {
          if (onSuccess) onSuccess();
        }, 1500);
        return true;
      } else {
        throw new Error(response.data.message || 'Failed to submit review');
      }
    } catch (err) {
      console.error('Error submitting review:', err);
      throw new Error(err.message || 'An error occurred while submitting review');
    }
  };
  
  // Initialize form using the useForm utility
  const { 
    formState, 
    errors, 
    isSubmitting, 
    submitError, 
    updateField, 
    submitForm, 
    resetForm 
  } = useForm(initialState, validateReviewForm, submitReview);
  
  // Star rating UI handlers
  const setRating = (value) => {
    updateField('rating', value);
  };
  
  const setHoverRating = (value) => {
    hoverRating.value = value;
  };
  
  const resetHoverRating = () => {
    hoverRating.value = 0;
  };
  
  return {
    user,
    formState,
    errors,
    isSubmitting,
    submitError,
    hoverRating,
    success,
    setRating,
    setHoverRating,
    resetHoverRating,
    submitForm,
    resetForm,
    updateField
  };
}