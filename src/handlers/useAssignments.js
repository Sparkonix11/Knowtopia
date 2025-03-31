import { ref } from 'vue';
import { getInstructorCoursesAPI, getEnrolledCoursesAPI, getSingleCourseAPI } from '../services/operations/courseAPI';

export function useAssignments() {
    const assignments = ref([]);
    const isLoading = ref(true);
    const error = ref(null);

    // Fetch assignments for instructors
    const fetchInstructorAssignments = async () => {
        try {
            // First get all courses created by the instructor
            const coursesResponse = await getInstructorCoursesAPI();
            
            if (coursesResponse.status !== 200) {
                throw new Error(coursesResponse.data?.error || 'Failed to fetch instructor courses');
            }
            
            const instructorCourses = coursesResponse.data.courses;
            const allAssignments = [];
            
            // For each course, get all weeks and their assignments
            for (const course of instructorCourses) {
                const courseResponse = await getSingleCourseAPI(course.id);
                
                if (courseResponse.status === 200) {
                    const courseData = courseResponse.data.course;
                    
                    for (const week of courseData.weeks) {
                        const weekAssignments = week.materials.filter(material => material.isAssignment);
                        weekAssignments.forEach(assignment => {
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
                        });
                    }
                }
            }
            
            assignments.value = allAssignments;
            return allAssignments;
        } catch (err) {
            console.error('Error fetching instructor assignments:', err);
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // Fetch assignments for students
    const fetchStudentAssignments = async () => {
        try {
            // First get all enrolled courses
            const coursesResponse = await getEnrolledCoursesAPI();
            
            if (coursesResponse.status !== 200) {
                throw new Error(coursesResponse.data?.error || 'Failed to fetch enrolled courses');
            }
            
            // The API returns enrolled_courses, not courses
            const enrolledCourses = coursesResponse.data.enrolled_courses || [];
            const allAssignments = [];
            
            // For each course, get all weeks and their assignments
            for (const course of enrolledCourses) {
                const courseResponse = await getSingleCourseAPI(course.id);
                
                if (courseResponse.status === 200) {
                    const courseData = courseResponse.data.course;
                    
                    for (const week of courseData.weeks) {
                        const weekAssignments = week.materials.filter(material => material.isAssignment);
                        weekAssignments.forEach(assignment => {
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
                        });
                    }
                }
            }
            
            assignments.value = allAssignments;
            return allAssignments;
        } catch (err) {
            console.error('Error fetching student assignments:', err);
            error.value = err.message;
            throw err;
        } finally {
            isLoading.value = false;
        }
    };

    // Format date for display
    const formatDueDate = (dateString) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', { weekday: 'short', year: 'numeric', month: 'short', day: 'numeric' });
    };

    return {
        assignments,
        isLoading,
        error,
        fetchInstructorAssignments,
        fetchStudentAssignments,
        formatDueDate
    };
}