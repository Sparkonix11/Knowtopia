// Mock data for testing charts

export const mockAverageMarks = [
  { id: 1, name: 'Quiz 1', courseName: 'Introduction to Programming', weekName: 'Week 1', averageScore: 85, submissionCount: 25 },
  { id: 2, name: 'Assignment 1', courseName: 'Data Structures', weekName: 'Week 2', averageScore: 72, submissionCount: 18 },
  { id: 3, name: 'Midterm', courseName: 'Algorithms', weekName: 'Week 4', averageScore: 78, submissionCount: 22 },
  { id: 4, name: 'Project', courseName: 'Web Development', weekName: 'Week 3', averageScore: 90, submissionCount: 15 },
  { id: 5, name: 'Final Exam', courseName: 'Introduction to Programming', weekName: 'Week 8', averageScore: 82, submissionCount: 24 }
];

export const mockStudentDoubts = [
  { id: 1, materialName: 'Arrays and Linked Lists', courseName: 'Data Structures', weekName: 'Week 2', doubtsCount: 15 },
  { id: 2, materialName: 'Recursion', courseName: 'Algorithms', weekName: 'Week 3', doubtsCount: 12 },
  { id: 3, materialName: 'HTML Basics', courseName: 'Web Development', weekName: 'Week 1', doubtsCount: 5 },
  { id: 4, materialName: 'CSS Styling', courseName: 'Web Development', weekName: 'Week 2', doubtsCount: 8 },
  { id: 5, materialName: 'JavaScript Functions', courseName: 'Web Development', weekName: 'Week 3', doubtsCount: 10 }
];

// Mock chart data functions
export function getMockMarksChartData() {
  return {
    labels: mockAverageMarks.map(assignment => `${assignment.name} (${assignment.courseName} - ${assignment.weekName})`),
    datasets: [{
      label: 'Average Marks (%)',
      data: mockAverageMarks.map(assignment => assignment.averageScore),
      backgroundColor: '#4361ee'
    }]
  };
}

export function getMockDoubtsChartData() {
  return {
    labels: mockStudentDoubts.map(material => `${material.materialName} (${material.courseName})`),
    datasets: [{
      label: 'Number of Doubts',
      data: mockStudentDoubts.map(material => material.doubtsCount),
      backgroundColor: '#4361ee'
    }]
  };
}