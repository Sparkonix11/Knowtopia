from flask_restful import Api
from .assignment import AssignmentResource, CreateAssignmentResource, DeleteAssignmentResource
from .submission import AssignmentSubmissionResource, AssignmentScoreResource
from .auth import SignupResource, LoginResource, LogoutResource
from .course import CourseResource, CreateCourseResource, InstructorCoursesResource, DeleteCourseResource, EnrolledCoursesResource, EnrollStudentResource, SingleCourseResource, CourseEditResource
from .material import MaterialResource, MaterialCreateResource, MaterialDeleteResource, MaterialEditResource
from .question import QuestionCreateResource, QuestionListResource, QuestionDeleteResource
from .review import ReviewResource, ReviewDeleteResource, InstructorReviewsResource
from .user import UserProfileResource, UserStudentListResource, DeleteUserResource
from .week import WeekCreateResource, WeekDeletionResource, WeekEditResource, WeekResource
from .ai import AskResource, QuestionHintResource, SummarizeResource
from .assignment_scores import AssignmentScoresResource, AllAssignmentScoresResource
from .material_doubts import MaterialDoubtCreateResource, MaterialDoubtsResource, AllMaterialDoubtsResource, StudentDoubtsResource
from .search import SearchResource
from .enrollment_request import EnrollmentRequestResource, StudentEnrollmentRequestsResource, InstructorEnrollmentRequestsResource, EnrollmentRequestActionResource


def init_routes(app):
    api = Api(app, prefix='/api/v1')

    # Assignment Routes
    api.add_resource(AssignmentResource, '/assignment/<int:assignment_id>')
    api.add_resource(CreateAssignmentResource, '/assignment/create/<int:week_id>')
    api.add_resource(DeleteAssignmentResource, '/assignment/delete/<int:assignment_id>')
    api.add_resource(AssignmentSubmissionResource, '/assignment/submit/<int:assignment_id>')
    api.add_resource(AssignmentScoreResource, '/assignment/score/<int:assignment_id>')
    
    # Assignment Scores Routes (for instructor dashboard)
    api.add_resource(AssignmentScoresResource, '/assignment/<int:assignment_id>/scores')
    api.add_resource(AllAssignmentScoresResource, '/assignment/all-scores')
    
    # Material Doubts Routes (for instructor dashboard)
    api.add_resource(MaterialDoubtCreateResource, '/material/<int:material_id>/doubt')
    api.add_resource(MaterialDoubtsResource, '/material/<int:material_id>/doubts')
    api.add_resource(AllMaterialDoubtsResource, '/material/all-doubts')
    api.add_resource(StudentDoubtsResource, '/material/student-doubts')

    # Auth Routes
    api.add_resource(SignupResource, '/auth/signup')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(LogoutResource, '/auth/logout')

    # Course Routes
    api.add_resource(CourseResource, '/course')
    api.add_resource(CreateCourseResource, '/course/create')
    api.add_resource(InstructorCoursesResource, '/course/instructor')
    api.add_resource(DeleteCourseResource, '/course/delete/<int:course_id>')
    api.add_resource(CourseEditResource, '/course/edit/<int:course_id>')
    api.add_resource(EnrolledCoursesResource, '/course/enrolled')
    api.add_resource(EnrollStudentResource, '/course/enroll/<int:course_id>/<int:student_id>')
    api.add_resource(SingleCourseResource, '/course/<int:course_id>')

    # Material Routes
    api.add_resource(MaterialResource, '/material/<int:material_id>')
    api.add_resource(MaterialCreateResource, '/material/create/<int:week_id>')
    api.add_resource(MaterialDeleteResource, '/material/delete/<int:material_id>')
    api.add_resource(MaterialEditResource, '/material/edit/<int:material_id>')


    # Question Routes
    api.add_resource(QuestionCreateResource, '/question/create/<int:assignment_id>')
    api.add_resource(QuestionListResource, '/question/<int:assignment_id>')
    api.add_resource(QuestionDeleteResource, '/question/delete/<int:question_id>')

    # Review Routes
    api.add_resource(ReviewResource, '/review/<int:material_id>')
    api.add_resource(ReviewDeleteResource, '/review/delete/<int:review_id>')
    api.add_resource(InstructorReviewsResource, '/review/instructor')

    # User Routes
    api.add_resource(UserProfileResource, '/user')
    api.add_resource(UserStudentListResource, '/user/students')
    api.add_resource(DeleteUserResource, '/user/delete/<int:user_id>')
    
    # Week Routes
    api.add_resource(WeekCreateResource, '/week/create/<int:course_id>')
    api.add_resource(WeekDeletionResource, '/week/delete/<int:course_id>/<int:week_id>')
    api.add_resource(WeekEditResource, '/week/edit/<int:course_id>/<int:week_id>')
    api.add_resource(WeekResource, '/week/<int:week_id>')

    # AI Routes
    api.add_resource(AskResource, '/ask')
    api.add_resource(QuestionHintResource, '/question_hint')
    api.add_resource(SummarizeResource, '/summarize')
    
    # Search Route
    api.add_resource(SearchResource, '/search')

    # Enrollment Request routes
    api.add_resource(EnrollmentRequestResource, '/enrollment-request')
    api.add_resource(StudentEnrollmentRequestsResource, '/enrollment-request/student')
    api.add_resource(InstructorEnrollmentRequestsResource, '/enrollment-request/instructor')
    api.add_resource(EnrollmentRequestActionResource, '/enrollment-request/<int:request_id>/action')