import { ref, computed } from 'vue';
import { getAllMaterialDoubtsAPI } from '../services/operations/materialDoubtAPI';

// Import API operations for assignment scores
import { getAllAssignmentScoresAPI } from '../services/operations/assignmentScoreAPI';

export function useInstructorDashboard() {
  // State for average marks data
  const averageMarks = ref([]);
  const isLoadingMarks = ref(false);
  const marksError = ref(null);
  
  // State for student doubts data
  const studentDoubts = ref([]);
  const isLoadingDoubts = ref(false);
  const doubtsError = ref(null);
  
  // Fetch average marks data for all assignments in instructor courses
  const fetchAverageMarks = async () => {
    try {
      isLoadingMarks.value = true;
      marksError.value = null;
      
      // Use the API operation to get all assignment scores for instructor's courses
      const response = await getAllAssignmentScoresAPI();
      
      if (response.status !== 200) {
        throw new Error(response.data?.error || 'Failed to fetch assignment scores');
      }
      
      // Get the assignments data with their scores
      const assignmentsData = response.data.assignments || [];
      
      // Format the data for the chart
      // We'll show each assignment with its course and week information
      const formattedData = assignmentsData.map(assignment => ({
        id: assignment.id,
        name: assignment.name,
        courseName: assignment.course_name,
        weekName: assignment.week_name,
        averageScore: assignment.average_percentage,
        submissionCount: assignment.submission_count,
        // Create a formatted label that includes course and week information
        label: `${assignment.name} (${assignment.course_name} - ${assignment.week_name})`
      }));
      
      // Sort by average score (descending)
      formattedData.sort((a, b) => b.averageScore - a.averageScore);
      
      // Take top 10 assignments with highest average scores
      const topAssignments = formattedData.slice(0, 10);
      
      averageMarks.value = topAssignments;
      return topAssignments;
    } catch (err) {
      console.error('Error fetching average marks:', err);
      marksError.value = err.message || 'Failed to load average marks';
      return [];
    } finally {
      isLoadingMarks.value = false;
    }
  };
  
  // Fetch student doubts data grouped by material/sublecture
  const fetchStudentDoubts = async () => {
    try {
      isLoadingDoubts.value = true;
      doubtsError.value = null;
      
      // Use the API operation to get all material doubts for instructor's courses
      const response = await getAllMaterialDoubtsAPI();
      
      if (response.status !== 200) {
        throw new Error(response.data?.error || 'Failed to fetch material doubts');
      }
      
      // Get the materials data with their doubts counts
      const materialsData = response.data.materials || [];
      
      // Format the data for the chart
      // We'll show each material with its course and week information
      const formattedData = materialsData.map(material => ({
        id: material.id,
        materialName: material.name,
        courseName: material.course_name,
        weekName: material.week_name,
        doubtsCount: material.doubts_count,
        // Create a formatted label that includes course information
        label: `${material.name} (${material.course_name})`
      }));
      
      // Sort by doubts count (descending)
      formattedData.sort((a, b) => b.doubtsCount - a.doubtsCount);
      
      // Take top 10 materials with most doubts
      const topDoubts = formattedData.slice(0, 10);
      
      studentDoubts.value = topDoubts;
      return topDoubts;
    } catch (err) {
      console.error('Error fetching student doubts:', err);
      doubtsError.value = err.message || 'Failed to load student doubts';
      return [];
    } finally {
      isLoadingDoubts.value = false;
    }
  };
  
  // Computed properties for chart data
  const marksChartData = computed(() => {
    return {
      labels: averageMarks.value.map(assignment => `${assignment.name} (${assignment.courseName} - ${assignment.weekName})`),
      datasets: [{
        label: 'Average Marks (%)',
        data: averageMarks.value.map(assignment => assignment.averageScore),
        backgroundColor: '#4361ee'
      }]
    };
  });
  
  const doubtsChartData = computed(() => {
    return {
      labels: studentDoubts.value.map(material => `${material.materialName} (${material.courseName})`),
      datasets: [{
        label: 'Number of Doubts',
        data: studentDoubts.value.map(material => material.doubtsCount),
        backgroundColor: '#4361ee'
      }]
    };
  });
  
  return {
    averageMarks,
    studentDoubts,
    isLoadingMarks,
    isLoadingDoubts,
    marksError,
    doubtsError,
    fetchAverageMarks,
    fetchStudentDoubts,
    marksChartData,
    doubtsChartData
  };
}