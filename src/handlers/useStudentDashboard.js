import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { apiConnector } from '../services/apiConnector';
import { assignmentEndpoints, materialEndpoints, courseEndpoints } from '../services/apis';
import { getStudentDoubtsAPI } from '../services/operations/materialDoubtAPI';

export function useStudentDashboard() {
  const store = useStore();
  
  // State for assignment marks data
  const assignmentMarks = ref([]);
  const isLoadingMarks = ref(false);
  const marksError = ref(null);
  
  // State for chat doubts data
  const chatDoubts = ref([]);
  const isLoadingDoubts = ref(false);
  const doubtsError = ref(null);
  
  // State for upcoming assignments
  const upcomingAssignments = ref([]);
  const isLoadingAssignments = ref(false);
  const assignmentsError = ref(null);
  
  // Fetch upcoming assignments with due dates
  const fetchUpcomingAssignments = async () => {
    try {
      isLoadingAssignments.value = true;
      assignmentsError.value = null;
      
      // Get enrolled courses from the API
      const coursesResponse = await apiConnector('GET', courseEndpoints.ENROLLED_COURSES);
      
      if (coursesResponse.status !== 200) {
        throw new Error(coursesResponse.data?.error || 'Failed to fetch enrolled courses');
      }
      
      const enrolledCourses = coursesResponse.data.enrolled_courses || [];
      const allAssignments = [];
      
      // For each course, get assignments with due dates
      for (const course of enrolledCourses) {
        const courseResponse = await apiConnector('GET', courseEndpoints.SINGLE_COURSE(course.id));
        
        if (courseResponse.status === 200) {
          const courseData = courseResponse.data.course;
          
          // Process each week to find assignments
          for (const week of courseData.weeks) {
            // Find materials that are assignments
            const weekAssignments = week.materials.filter(material => material.isAssignment);
            
            // Add course and week info to each assignment
            weekAssignments.forEach(assignment => {
              if (assignment.due_date) {
                allAssignments.push({
                  id: assignment.assignment_id,
                  name: assignment.material_name,
                  description: assignment.description || '',
                  due_date: assignment.due_date,
                  courseId: course.id,
                  courseName: course.name,
                  weekId: week.id,
                  weekName: week.name
                });
              }
            });
          }
        }
      }
      
      // Sort assignments by due date (ascending)
      allAssignments.sort((a, b) => {
        const dateA = new Date(a.due_date);
        const dateB = new Date(b.due_date);
        return dateA - dateB;
      });
      
      // Filter to only show upcoming assignments (due date >= today)
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      
      const upcoming = allAssignments.filter(assignment => {
        const dueDate = new Date(assignment.due_date);
        return dueDate >= today;
      });
      
      upcomingAssignments.value = upcoming;
      return upcoming;
    } catch (err) {
      console.error('Error fetching upcoming assignments:', err);
      assignmentsError.value = err.message || 'Failed to load upcoming assignments';
      return [];
    } finally {
      isLoadingAssignments.value = false;
    }
  };
  
  // Fetch assignment marks data
  const fetchAssignmentMarks = async () => {
    try {
      isLoadingMarks.value = true;
      marksError.value = null;
      
      // Get enrolled courses from the store or API
      const coursesResponse = await apiConnector('GET', 'http://127.0.0.1:5000/api/v1/course/enrolled');
      
      if (coursesResponse.status !== 200) {
        throw new Error(coursesResponse.data?.error || 'Failed to fetch enrolled courses');
      }
      
      const enrolledCourses = coursesResponse.data.enrolled_courses || [];
      const allAssignments = [];
      
      // For each course, get assignments and their scores
      for (const course of enrolledCourses) {
        const courseResponse = await apiConnector('GET', `http://127.0.0.1:5000/api/v1/course/${course.id}`);
        
        if (courseResponse.status === 200) {
          const courseData = courseResponse.data.course;
          
          // Process each week to find assignments
          for (const week of courseData.weeks) {
            // Find materials that are assignments
            const weekAssignments = week.materials.filter(material => material.isAssignment);
            
            // For each assignment, get the score
            for (const assignment of weekAssignments) {
              try {
                const scoreResponse = await apiConnector('GET', assignmentEndpoints.GET_ASSIGNMENT_SCORE(assignment.assignment_id));
                
                if (scoreResponse.status === 200 && scoreResponse.data.score) {
                  allAssignments.push({
                    id: assignment.assignment_id,
                    name: assignment.material_name,
                    courseName: courseData.name,
                    score: scoreResponse.data.score.percentage,
                    topic: courseData.name // Using course name as topic for simplicity
                  });
                }
              } catch (err) {
                console.error(`Error fetching score for assignment ${assignment.assignment_id}:`, err);
                // Continue with next assignment even if one fails
              }
            }
          }
        }
      }
      
      assignmentMarks.value = allAssignments;
      return allAssignments;
    } catch (err) {
      console.error('Error fetching assignment marks:', err);
      marksError.value = err.message || 'Failed to load assignment marks';
      return [];
    } finally {
      isLoadingMarks.value = false;
    }
  };
  
  // Fetch chat doubts data from the backend API
  const fetchChatDoubts = async () => {
    try {
      isLoadingDoubts.value = true;
      doubtsError.value = null;
      
      // Get doubts data from the API
      const response = await getStudentDoubtsAPI();
      
      if (response.status !== 200) {
        throw new Error(response.data?.error || 'Failed to fetch doubts data');
      }
      
      // Get the doubts by day data
      const doubtsData = response.data.doubts_by_day || [];
      
      // Format the data for the chart
      const formattedData = doubtsData.map((item, index) => ({
        day: index + 1, // Day number (1-10)
        date: item.date, // Date string
        count: item.count // Number of doubts
      }));
      
      chatDoubts.value = formattedData;
      return formattedData;
    } catch (err) {
      console.error('Error fetching chat doubts:', err);
      doubtsError.value = err.message || 'Failed to load doubts data';
      return [];
    } finally {
      isLoadingDoubts.value = false;
    }
  };
  
  // Computed properties for chart data
  const marksChartData = computed(() => {
    return {
      labels: assignmentMarks.value.map(a => a.topic),
      datasets: [{
        label: 'Marks (%)',
        data: assignmentMarks.value.map(a => a.score),
        backgroundColor: '#4361ee'
      }]
    };
  });
  
  const doubtsChartData = computed(() => {
    return {
      labels: chatDoubts.value.map(d => `Day ${d.day}`),
      datasets: [{
        label: 'Doubts Asked',
        data: chatDoubts.value.map(d => d.count),
        borderColor: '#4361ee',
        tension: 0.1,
        fill: false
      }]
    };
  });
  
  return {
    assignmentMarks,
    chatDoubts,
    upcomingAssignments,
    isLoadingMarks,
    isLoadingDoubts,
    isLoadingAssignments,
    marksError,
    doubtsError,
    assignmentsError,
    fetchAssignmentMarks,
    fetchChatDoubts,
    fetchUpcomingAssignments,
    marksChartData,
    doubtsChartData
  };
}