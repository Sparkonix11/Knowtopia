/**
 * Form validation utility functions
 */

/**
 * Checks if a value is not empty
 * 
 * @param {string} value - The value to check
 * @returns {boolean} Whether the value is not empty
 */
export function isNotEmpty(value) {
  return value !== undefined && value !== null && value.trim() !== '';
}

/**
 * Validates an email address format
 * 
 * @param {string} email - The email to validate
 * @returns {boolean} Whether the email is valid
 */
export function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

/**
 * Validates a phone number format
 * 
 * @param {string} phone - The phone number to validate
 * @returns {boolean} Whether the phone number is valid
 */
export function isValidPhone(phone) {
  // Basic phone validation - can be customized based on requirements
  const phoneRegex = /^\d{10,15}$/;
  return phoneRegex.test(phone.replace(/[\s()-]/g, ''));
}

/**
 * Validates password strength
 * 
 * @param {string} password - The password to validate
 * @returns {boolean} Whether the password meets strength requirements
 */
export function isStrongPassword(password) {
  // At least 8 characters, containing at least one number and one letter
  return password.length >= 8 && /[0-9]/.test(password) && /[a-zA-Z]/.test(password);
}

/**
 * Validates that two passwords match
 * 
 * @param {string} password - The password
 * @param {string} confirmPassword - The confirmation password
 * @returns {boolean} Whether the passwords match
 */
export function passwordsMatch(password, confirmPassword) {
  return password === confirmPassword;
}

/**
 * Creates a validation result object
 * 
 * @param {boolean} isValid - Whether the validation passed
 * @param {Object} errors - The validation errors
 * @returns {Object} The validation result
 */
export function createValidationResult(isValid, errors = {}) {
  return {
    isValid,
    errors
  };
}