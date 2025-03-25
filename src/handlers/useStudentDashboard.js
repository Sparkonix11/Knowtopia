import { ref, computed } from 'vue';
import { useStore } from 'vuex';
import { apiConnector } from '../services/apiConnector';
import { assignmentEndpoints } from '../services/apis';

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
  
  // Fetch chat doubts data from the chat store
  const fetchChatDoubts = async () => {
    try {
      isLoadingDoubts.value = true;
      doubtsError.value = null;
      
      // Get chat history from the store
      const conversations = store.state.chat.conversations;
      
      // Process chat data to count doubts per day
      const doubtsPerDay = {};
      const today = new Date();
      
      // Initialize the last 10 days with 0 doubts
      for (let i = 9; i >= 0; i--) {
        const date = new Date(today);
        date.setDate(today.getDate() - i);
        const dateString = date.toISOString().split('T')[0]; // Format: YYYY-MM-DD
        doubtsPerDay[dateString] = 0;
      }
      
      // Count user messages (doubts) per day
      Object.values(conversations).forEach(conversation => {
        conversation.forEach(message => {
          if (message.isUser) {
            const messageDate = new Date(message.timestamp).toISOString().split('T')[0];
            if (doubtsPerDay[messageDate] !== undefined) {
              doubtsPerDay[messageDate]++;
            }
          }
        });
      });
      
      // Convert to array format for chart.js
      const doubtsData = Object.entries(doubtsPerDay).map(([date, count], index) => ({
        day: index + 1, // Day number (1-10)
        date, // Full date string
        count // Number of doubts
      }));
      
      chatDoubts.value = doubtsData;
      return doubtsData;
    } catch (err) {
      console.error('Error processing chat doubts:', err);
      doubtsError.value = err.message || 'Failed to process chat data';
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
    isLoadingMarks,
    isLoadingDoubts,
    marksError,
    doubtsError,
    fetchAssignmentMarks,
    fetchChatDoubts,
    marksChartData,
    doubtsChartData
  };
}