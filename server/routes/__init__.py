from flask_restful import Api
from .assignment import AssignmentResource, CreateAssignmentResource, DeleteAssignmentResource
from .auth import SignupResource, LoginResource, LogoutResource, UserProfileResource
from .course import CourseResource, CreateCourseResource, InstructorCoursesResource, DeleteCourseResource
from .material import MaterialCreateResource, MaterialDeleteResource
from .question import QuestionCreateResource, QuestionListResource, QuestionDeleteResource
from .review import ReviewResource
from .week import WeekCreateResource, WeekDeletionResource
from .ai import AskResource, QuestionHintResource

def init_routes(app):
    api = Api(app, prefix='/api/v1')

    # Assignment Routes
    api.add_resource(AssignmentResource, '/assignment/<int:assignment_id>')
    api.add_resource(CreateAssignmentResource, '/assignment/create/<int:week_id>')
    api.add_resource(DeleteAssignmentResource, '/assignment/delete/<int:assignment_id>')

    # Auth Routes
    api.add_resource(SignupResource, '/auth/signup')
    api.add_resource(LoginResource, '/auth/login')
    api.add_resource(LogoutResource, '/auth/logout')
    api.add_resource(UserProfileResource, '/user')

    # Course Routes
    api.add_resource(CourseResource, '/course')
    api.add_resource(CreateCourseResource, '/course/create')
    api.add_resource(InstructorCoursesResource, '/course/instructor')
    api.add_resource(DeleteCourseResource, '/course/delete/<int:course_id>')

    # Material Routes
    api.add_resource(MaterialCreateResource, '/material/create/<int:week_id>')
    api.add_resource(MaterialDeleteResource, '/material/delete/<int:material_id>')


    # Question Routes
    api.add_resource(QuestionCreateResource, '/question/create/<int:assignment_id>')
    api.add_resource(QuestionListResource, '/question/<int:assignment_id>')
    api.add_resource(QuestionDeleteResource, '/question/delete/<int:question_id>')

    # Review Routes
    api.add_resource(ReviewResource, '/review/<int:material_id>')

    # Week Routes
    api.add_resource(WeekCreateResource, '/week/create/<int:course_id>')
    api.add_resource(WeekDeletionResource, '/week/delete/<int:course_id>/<int:week_id>')

    # AI Routes
    api.add_resource(AskResource, '/ask')
    api.add_resource(QuestionHintResource, '/question_hint')