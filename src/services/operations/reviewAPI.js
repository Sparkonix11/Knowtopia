import { apiConnector } from "../apiConnector";
import { reviewEndpoints } from "../apis";

export async function submitReviewAPI(payload) {
  try {
    const { materialId, rating, comment } = payload;
    
    // Create FormData object instead of sending JSON
    const formData = new FormData();
    formData.append('rating', rating);
    formData.append('comment', comment);
    
    // Pass formData as the body and set appropriate headers
    const response = await apiConnector("POST", reviewEndpoints.REVIEW(materialId), formData);
    return response;
  } catch (error) {
    throw error;
  }
}

export async function fetchReviewsAPI(materialId) {
  try {
    const response = await apiConnector("GET", reviewEndpoints.REVIEW(materialId));
    return response;
  } catch (error) {
    throw error;
  }
}

export async function deleteReviewAPI(reviewId) {
  try {
    const response = await apiConnector("DELETE", reviewEndpoints.DELETE_REVIEW(reviewId));
    return response;
  } catch (error) {
    throw error;
  }
}