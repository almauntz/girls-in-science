<template>
  <div class="max-w-3xl mx-auto px-6 py-10">
    <div v-if="loading" class="text-center text-gray-500">Učitavanje...</div>
    <div v-else-if="error" class="text-center text-red-500">{{ error }}</div>
    <div v-else-if="newsPost">
      <div class="bg-white rounded-3xl shadow-lg p-8">
        <div class="flex items-center justify-between mb-8">
          <router-link
            to="/news"
            class="inline-flex items-center gap-2 px-4 py-2 bg-white text-primary rounded-xl shadow-sm hover:shadow-md border border-gray-100 transition"
          >
            ← Nazad na novosti
          </router-link>

          <div v-if="isAdmin" class="flex gap-3">
            <router-link
              :to="`/news/${newsPost.id}/edit`"
              class="bg-primary hover:bg-secondary text-white px-5 py-2 rounded-xl font-medium transition"
            >
              Uredi
            </router-link>
            <button
              @click="handleDelete"
              class="bg-red-600 hover:bg-red-700 text-white font-medium px-5 py-2 rounded-xl transition"
            >
              Obriši
            </button>
          </div>
        </div>

        <img
          v-if="newsPost.image_url"
          :src="`http://localhost:8000${newsPost.image_url}`"
          class="w-full rounded-2xl mb-8 object-cover max-h-[450px] shadow-md"
        />

        <div class="mb-6">
          <h1 class="text-4xl font-bold text-gray-900 mb-2 break-all">
            {{ newsPost.title }}
          </h1>
          <p class="text-gray-500">
            {{ formatDate(newsPost.created_at) }}
          </p>
          <p v-if="newsPost.author" class="text-gray-500 mt-1">
            Autor: {{ newsPost.author }}
          </p>
        </div>
        <div
          v-if="newsPost.categories?.length"
          class="flex flex-wrap gap-2 mt-4"
        >
          <span
            v-for="category in newsPost.categories"
            :key="category.id"
            class="px-3 py-1 rounded-full bg-primary text-white text-sm font-medium"
          >
            {{ category.name }}
          </span>
        </div>

        <div class="border border-gray-100 rounded-2xl p-6 mb-6 mt-4">
          <h2 class="text-l font-bold text-gray-900 mb-4">Sadržaj</h2>
          <p
            class="text-gray-700 whitespace-pre-line leading-relaxed break-words"
          >
            {{ newsPost.content }}
          </p>
        </div>

        <div v-if="newsPost.role_models && newsPost.role_models.length > 0">
          <h2 class="text-lg font-semibold text-gray-900 mb-3">
            Povezani profili
          </h2>
          <div class="flex flex-col gap-3">
            <div
              v-for="model in newsPost.role_models"
              :key="model.id"
              @click="$router.push({ path: `/role-models/${model.id}`, query: { from: 'news', newsId: newsPost.id } })"
              class="flex items-center gap-4 bg-white border border-gray-100 rounded-2xl p-4 cursor-pointer hover:shadow-lg transition"
            >
              <div class="w-12 h-12 flex-shrink-0">
                <img
                  v-if="model.image_url"
                  :src="`http://localhost:8000${model.image_url}`"
                  class="w-12 h-12 rounded-full object-cover"
                />
                <div
                  v-else
                  class="w-12 h-12 rounded-full bg-primary text-white flex items-center justify-center font-bold"
                >
                  {{ getInitials(model.first_name, model.last_name) }}
                </div>
              </div>
              <div>
                <p class="font-semibold text-gray-900">
                  {{ model.first_name }} {{ model.last_name }}
                </p>
                <p class="text-sm text-primary font-medium">
                  {{ model.stem_field }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- Komentari -->
        <div class="mt-8">
          <h2 class="text-lg font-semibold text-gray-900 mb-4">
            Komentari ({{ comments.length }})
          </h2>

          <div v-if="comments.length === 0" class="text-gray-500 text-sm mb-6">
            Još nema komentara. Budite prvi!
          </div>

          <div class="flex flex-col gap-4 mb-6">
            <div
              v-for="comment in comments"
              :key="comment.id"
              class="border border-gray-100 rounded-2xl p-4"
            >
              <div class="flex items-center justify-between mb-2">
                <div>
                  <p class="font-semibold text-gray-900 text-sm">{{ comment.user_full_name }}</p>
                  <p class="text-xs text-gray-400">{{ formatDate(comment.created_at) }}</p>
                </div>
                <button
                  v-if="isAdmin || comment.user_id === currentUserId"
                  @click="handleDeleteComment(comment.id)"
                  class="text-red-500 hover:text-red-700 text-xs transition"
                >
                  Obriši
                </button>
              </div>
              <p class="text-gray-700 text-sm">{{ comment.content }}</p>
            </div>
          </div>

          <div v-if="isLoggedIn" class="flex gap-3">
            <input
              v-model="newComment"
              type="text"
              placeholder="Napišite komentar..."
              class="flex-1 border border-gray-300 rounded-xl px-4 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary"
            />
            <button
              @click="handleCreateComment"
              class="bg-primary hover:bg-secondary text-white px-4 py-2 rounded-xl text-sm transition"
            >
              Pošalji
            </button>
          </div>
          <p v-else class="text-sm text-gray-400">
            <router-link to="/login" class="text-primary hover:underline">Prijavite se</router-link>
            da biste ostavili komentar.
          </p>
        </div>

      </div>
    </div>
  </div>
</template>
   
<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import { getNewsPost, deleteNewsPost, getMe, getComments, createComment, deleteComment } from "../../services/api.js";
import Swal from "sweetalert2";

const route = useRoute();
const router = useRouter();
const newsPost = ref(null);
const loading = ref(true);
const error = ref(null);
const isAdmin = ref(false);
const isLoggedIn = ref(false);
const currentUserId = ref(null);
const comments = ref([]);
const newComment = ref('');

function getInitials(first, last) {
  return `${first?.[0] || ""}${last?.[0] || ""}`.toUpperCase();
}

function formatDate(dateStr) {
  if (!dateStr) return "";
  return new Date(dateStr).toLocaleDateString("bs-BA", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
}

async function handleDelete() {
  const result = await Swal.fire({
    title: "Obriši objavu",
    text: "Da li ste sigurni da želite obrisati ovu objavu?",
    icon: "warning",
    showCancelButton: true,
    confirmButtonColor: "#7c3aed",
    cancelButtonColor: "#6b7280",
    confirmButtonText: "Obriši",
    cancelButtonText: "Odustani",
  });
  if (!result.isConfirmed) return;
  const token = localStorage.getItem("token");
  const deleteResult = await deleteNewsPost(newsPost.value.id, token);
  if (deleteResult.message) {
    router.push("/news");
  }
}

async function handleCreateComment() {
  if (!newComment.value.trim()) return;
  const result = await createComment(route.params.id, { content: newComment.value.trim() });
  if (result.id) {
    comments.value.push(result);
    newComment.value = '';
  }
}

async function handleDeleteComment(commentId) {
  const result = await deleteComment(route.params.id, commentId);
  if (result.message) {
    comments.value = comments.value.filter(c => c.id !== commentId);
  }
}

onMounted(async () => {
  try {
    const token = localStorage.getItem("token");
    if (token) {
      const user = await getMe(token);
      isAdmin.value = user.role === "admin";
      isLoggedIn.value = true;
      currentUserId.value = user.id;
    }
    const data = await getNewsPost(route.params.id);
    if (data.detail) {
      error.value = "Objava nije pronađena.";
    } else {
      newsPost.value = data;
      const commentsData = await getComments(route.params.id);
      comments.value = Array.isArray(commentsData) ? commentsData : [];
    }
  } catch {
    error.value = "Došlo je do greške pri učitavanju objave.";
  } finally {
    loading.value = false;
  }
});
</script>
