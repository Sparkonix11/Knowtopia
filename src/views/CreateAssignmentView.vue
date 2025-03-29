<script setup>
import { onMounted } from 'vue';
import NavbarMain from '@/components/NavbarMain.vue';
import Sidebar from '@/components/Sidebar.vue';
import { useRouter } from 'vue-router';
import { useCreateAssignment } from '@/handlers/useCreateAssignment';

const router = useRouter();

// Use the assignment handler
const {
  title,
  description,
  dueDate,
  questions,
  formErrors,
  isLoading,
  isLoadingCourses,
  error,
  success,
  courses,
  selectedCourse,
  weeks,
  selectedWeek,
  addQuestion,
  removeQuestion,
  validateForm,
  createAssignment,
  fetchCourses
} = useCreateAssignment();

// Fetch courses on component mount
onMounted(() => {
  fetchCourses();
});

// Submit form
const submitForm = async () => {
  const result = await createAssignment();
  if (result) {
    // Redirect back to course view after a short delay
    setTimeout(() => {
      router.push({ name: 'Course' });
    }, 2000);
  }
};

// Cancel and go back
const cancelForm = () => {
  router.go(-1);
};
</script>

<template>
  <NavbarMain />
  <div class="flex">
    <Sidebar />
    <div class="flex-1 p-8">
      <div class="max-w-4xl mx-auto bg-(--md-sys-color-surface-container) p-6 rounded-lg shadow">
        <h1 class="text-2xl font-bold mb-6">Create Assignment</h1>
        
        <!-- Error and Success Messages -->
        <div v-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {{ error }}
        </div>
        
        <div v-if="success" class="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-4">
          {{ success }}
        </div>
        
        <form @submit.prevent="submitForm">
          <!-- Course Selection -->
          <div class="mb-4">
            <label for="course" class="block text-sm font-medium mb-1">Select Course</label>
            <select
              id="course"
              v-model="selectedCourse"
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': formErrors.course}"
              :disabled="isLoadingCourses"
            >
              <option :value="null">Select a course</option>
              <option v-for="course in courses" :key="course.id" :value="course">{{ course.name }}</option>
            </select>
            <p v-if="formErrors.course" class="text-red-500 text-sm mt-1">{{ formErrors.course }}</p>
          </div>
          
          <!-- Week Selection -->
          <div class="mb-4">
            <label for="week" class="block text-sm font-medium mb-1">Select Week</label>
            <select
              id="week"
              v-model="selectedWeek"
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': formErrors.week}"
              :disabled="!selectedCourse || weeks.length === 0"
            >
              <option :value="null">Select a week</option>
              <option v-for="week in weeks" :key="week.id" :value="week">{{ week.name }}</option>
            </select>
            <p v-if="formErrors.week" class="text-red-500 text-sm mt-1">{{ formErrors.week }}</p>
            <p v-if="selectedCourse && weeks.length === 0" class="text-yellow-600 text-sm mt-1">
              No weeks available for this course. Please create a week first.
            </p>
          </div>
          
          <!-- Assignment Title -->
          <div class="mb-4">
            <label for="title" class="block text-sm font-medium mb-1">Assignment Title</label>
            <input 
              type="text" 
              id="title" 
              v-model="title" 
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': formErrors.title}"
            >
            <p v-if="formErrors.title" class="text-red-500 text-sm mt-1">{{ formErrors.title }}</p>
          </div>
          
          <!-- Assignment Description -->
          <div class="mb-6">
            <label for="description" class="block text-sm font-medium mb-1">Description</label>
            <textarea 
              id="description" 
              v-model="description" 
              rows="3" 
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': formErrors.description}"
            ></textarea>
            <p v-if="formErrors.description" class="text-red-500 text-sm mt-1">{{ formErrors.description }}</p>
          </div>
          
          <!-- Due Date -->
          <div class="mb-6">
            <label for="dueDate" class="block text-sm font-medium mb-1">Due Date</label>
            <input 
              type="datetime-local" 
              id="dueDate" 
              v-model="dueDate" 
              class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
              :class="{'border-red-500': formErrors.dueDate}"
            >
            <p v-if="formErrors.dueDate" class="text-red-500 text-sm mt-1">{{ formErrors.dueDate }}</p>
          </div>
          
          <!-- Questions Section -->
          <div class="mb-6">
            <div class="flex justify-between items-center mb-4">
              <h2 class="text-xl font-semibold">Questions</h2>
              <md-filled-button type="button" @click="addQuestion" class="w-34 h-12">
                Add Question
              </md-filled-button>
            </div>
            
            <!-- Question Cards -->
            <div v-for="(question, index) in questions" :key="index" class="bg-(--md-sys-color-surface) p-4 rounded-lg mb-4 shadow-sm">
              <div class="flex justify-between items-center mb-3">
                <h3 class="font-medium">Question {{ index + 1 }}</h3>
                <md-icon-button v-if="questions.length > 1" @click="removeQuestion(index)">
                  <md-icon>delete</md-icon>
                </md-icon-button>
              </div>
              
              <!-- Question Text -->
              <div class="mb-3">
                <label :for="`question-${index}`" class="block text-sm font-medium mb-1">Question</label>
                <input 
                  :id="`question-${index}`" 
                  type="text" 
                  v-model="question.question_description" 
                  class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                  :class="{'border-red-500': formErrors.questions[index]?.question_description}"
                >
                <p v-if="formErrors.questions[index]?.question_description" class="text-red-500 text-sm mt-1">
                  {{ formErrors.questions[index].question_description }}
                </p>
              </div>
              
              <!-- Options -->
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 mb-3">
                <div v-for="optionNum in 4" :key="optionNum">
                  <label :for="`option${optionNum}-${index}`" class="block text-sm font-medium mb-1">
                    Option {{ optionNum }}
                  </label>
                  <div class="flex items-center">
                    <input 
                      type="radio" 
                      :id="`correct-${index}-${optionNum}`" 
                      :name="`correct-${index}`" 
                      :value="optionNum.toString()" 
                      v-model="question.correct_option"
                      class="mr-2"
                    >
                    <input 
                      :id="`option${optionNum}-${index}`" 
                      type="text" 
                      v-model="question[`option${optionNum}`]" 
                      class="flex-1 p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500"
                      :class="{'border-red-500': formErrors.questions[index]?.[`option${optionNum}`]}"
                    >
                  </div>
                  <p v-if="formErrors.questions[index]?.[`option${optionNum}`]" class="text-red-500 text-sm mt-1">
                    {{ formErrors.questions[index][`option${optionNum}`] }}
                  </p>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Form Actions -->
          <div class="flex justify-end space-x-4">
            <md-outlined-button type="button" @click="cancelForm" class="w-24 h-12">Cancel</md-outlined-button>
            <md-filled-button type="submit" :disabled="isLoading" class="w-40 h-12">
              <md-circular-progress v-if="isLoading" indeterminate></md-circular-progress>
              <span v-else>Create Assignment</span>
            </md-filled-button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>