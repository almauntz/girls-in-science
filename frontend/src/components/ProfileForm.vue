<template>
  <div>
    <!-- Header -->
    <div class="relative w-full rounded-xl mb-6 overflow-hidden" style="background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 50%, #9333ea 100%); min-height: 170px;">
      <div class="absolute top-4 right-4">
        <button v-if="!isEditMode && activeTab === 'info'" type="button" @click="isEditMode = true"
          class="text-sm text-violet-700 bg-white hover:bg-violet-50 font-medium px-4 py-2 rounded-lg transition-colors flex items-center gap-2">
          ✏️ Edit Profile
        </button>
      </div>
      <div class="absolute w-full left-0 bottom-4 px-6 flex items-end gap-6">
        <div class="relative flex-shrink-0" :class="isEditMode ? 'cursor-pointer group' : ''" @click="isEditMode && $refs.fileInput.click()">
          <div class="w-32 h-32 rounded-3xl border-4 border-white bg-violet-400 flex items-center justify-center overflow-hidden shadow-lg">
            <img v-if="avatarUrl" :src="avatarUrl" alt="Avatar" class="w-full h-full object-cover" />
            <span v-else class="text-5xl">👤</span>
          </div>
          <div class="absolute inset-0 rounded-3xl bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center">
            <span class="text-white text-xl opacity-0 group-hover:opacity-100">📷</span>
          </div>
          <div v-if="isUploading" class="absolute inset-0 rounded-3xl bg-black bg-opacity-40 flex items-center justify-center">
            <span class="text-white text-xs">...</span>
          </div>
          <button v-if="avatarUrl && isEditMode" type="button" @click.stop="handleDeleteAvatar"
            class="absolute -top-1 -right-1 w-6 h-6 bg-red-500 hover:bg-red-600 text-white rounded-full flex items-center justify-center text-xs transition-colors z-10">✕</button>
        </div>
        <input ref="fileInput" type="file" accept=".jpg,.jpeg,.png" class="hidden" @change="handleAvatarChange" />
        <div class="mb-2 flex flex-col gap-1">
          <div class="flex items-center gap-3">
            <h2 class="text-3xl font-bold text-white leading-none">{{ fullName || 'Korisnice' }}</h2>
            <span class="bg-white/20 text-white text-[10px] font-bold px-2.5 py-1 rounded-full uppercase tracking-wider">
              <span v-if="userRole === 'admin'">Administrator</span>
              <span v-else-if="userRole === 'mentor'">Mentorica</span>
              <span v-else>Studentica</span>
            </span>
          </div>
          <p class="text-violet-100 text-sm font-medium">{{ form.field || 'Oblast nije unesena' }}</p>
          <p v-if="avatarError" class="text-red-200 text-xs mt-1">{{ avatarError }}</p>
        </div>
      </div>
    </div>

    <!-- Tabovi -->
    <div class="flex border-b border-gray-200 mb-6">
      <button @click="activeTab = 'info'" :class="['px-6 py-3 text-sm font-medium border-b-2 transition-colors', activeTab === 'info' ? 'border-violet-600 text-violet-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
        Profil i Biografija
      </button>
      <button @click="activeTab = 'security'" :class="['px-6 py-3 text-sm font-medium border-b-2 transition-colors', activeTab === 'security' ? 'border-violet-600 text-violet-600' : 'border-transparent text-gray-500 hover:text-gray-700']">
        Sigurnost i Lozinka
      </button>
    </div>

    <div v-if="activeTab === 'info'">
      <div v-if="successMessage" class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">{{ successMessage }}</div>
      <div v-if="errorMessage" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">{{ errorMessage }}</div>

      <form @submit.prevent="saveProfile" class="space-y-6">

        <!-- RED 1: Osobne info + Oblast/Biografija -->
        <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 items-start">

          <!-- Lijeva kolona -->
          <div class="lg:col-span-1 space-y-6">

            <!-- Osobne informacije -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-5">
                <span class="text-violet-500">👤</span>
                <h3 class="text-sm font-semibold text-gray-800">Osobne informacije</h3>
              </div>
              <div>
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Ime i prezime</label>
                <p v-if="!isEditMode" class="text-sm font-medium text-gray-800">{{ form.full_name || 'Nije uneseno' }}</p>
                <input v-else v-model="form.full_name" type="text" placeholder="Unesite ime i prezime"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                <p v-if="errors.full_name" class="text-red-500 text-xs mt-1">{{ errors.full_name }}</p>
              </div>
            </div>

            <!-- Kontakt podaci -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-5">
                <span class="text-violet-500">✉️</span>
                <h3 class="text-sm font-semibold text-gray-800">Kontakt Podaci</h3>
              </div>
              <div class="mb-4">
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Email adresa</label>
                <p v-if="!isEditMode" class="text-sm font-medium text-gray-800">{{ form.email || 'Nije uneseno' }}</p>
                <input v-else v-model="form.email" type="text" placeholder="Npr. tvoj@email.com"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                <p v-if="errors.email" class="text-red-500 text-xs mt-1">{{ errors.email }}</p>
              </div>
              <div>
                <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Lokacija</label>
                <p v-if="!isEditMode" class="text-sm font-medium text-gray-800">{{ form.location || 'Nije uneseno' }}</p>
                <input v-else v-model="form.location" type="text" placeholder="Npr. Sarajevo, BiH"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
              </div>
            </div>

            <!-- Društvene mreže -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-5">
                <span class="text-violet-500">🔗</span>
                <h3 class="text-sm font-semibold text-gray-800">Društvene mreže</h3>
              </div>
              <div class="space-y-3">
                <div>
                  <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">LinkedIn</label>
                  <p v-if="!isEditMode" class="text-sm text-gray-700">{{ form.linkedin_url || 'Nije uneseno' }}</p>
                  <input v-else v-model="form.linkedin_url" type="text" placeholder="https://linkedin.com/in/..."
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                </div>
                <div>
                  <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">GitHub</label>
                  <p v-if="!isEditMode" class="text-sm text-gray-700">{{ form.github_url || 'Nije uneseno' }}</p>
                  <input v-else v-model="form.github_url" type="text" placeholder="https://github.com/..."
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                </div>
                <div>
                  <label class="text-[10px] font-bold text-gray-400 uppercase tracking-wider block mb-1">Twitter / X</label>
                  <p v-if="!isEditMode" class="text-sm text-gray-700">{{ form.twitter_url || 'Nije uneseno' }}</p>
                  <input v-else v-model="form.twitter_url" type="text" placeholder="https://x.com/..."
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                </div>
              </div>
            </div>

          </div>

          <!-- Desna kolona -->
          <div class="lg:col-span-2 space-y-6">

            <!-- Oblast -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-violet-500">📚</span>
                <h3 class="text-sm font-semibold text-gray-800">Primarna Naučna Oblast</h3>
              </div>
              <p class="text-xs text-gray-400 mb-4 ml-6">Izaberite svoj primarni fokus istraživanja i usmjerenja</p>
              <p v-if="!isEditMode" class="text-sm font-medium text-gray-800 px-4 py-3 bg-gray-50 rounded-xl border border-gray-100">
                {{ form.field || 'Nije odabrano' }}
              </p>
              <select v-else v-model="form.field"
                class="w-full border border-gray-300 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white appearance-none">
                <option value="" disabled>Izaberite oblast...</option>
                <option v-for="f in fields" :key="f" :value="f">{{ f }}</option>
              </select>
            </div>

            <!-- Biografija -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6 flex flex-col">
              <div class="flex items-center gap-2 mb-5">
                <span class="text-violet-500">📖</span>
                <h3 class="text-sm font-semibold text-gray-800">Biografija</h3>
              </div>
              <div v-if="!isEditMode" class="border-l-4 border-violet-200 pl-4 py-1 mb-4 min-h-[120px]">
                <p class="text-sm text-gray-600 italic leading-relaxed whitespace-pre-wrap">"{{ form.biography || 'Nije uneseno' }}"</p>
              </div>
              <div v-else>
                <textarea v-model="form.biography" placeholder="Napišite nešto o sebi..." rows="8" spellcheck="false"
                  class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 resize-none"></textarea>
                <div class="flex justify-between mt-1">
                  <p v-if="errors.biography" class="text-red-500 text-xs">{{ errors.biography }}</p>
                  <span class="text-xs text-gray-400 ml-auto">{{ form.biography?.length || 0 }}/500</span>
                </div>
              </div>
              <!-- Privacy -->
              <div v-if="isEditMode" class="mt-4 pt-4 border-t border-gray-100">
                <div class="flex items-center gap-2 mb-3">
                  <span class="text-violet-500">🔒</span>
                  <h3 class="text-sm font-semibold text-gray-800">Privatnost — šta je javno vidljivo</h3>
                </div>
                <div class="space-y-2">
                  <label class="flex items-center justify-between gap-3 cursor-pointer">
                    <span class="text-sm text-gray-600">Prikaži biografiju</span>
                    <input type="checkbox" v-model="form.show_biography" class="w-4 h-4 accent-violet-600"/>
                  </label>
                  <label class="flex items-center justify-between gap-3 cursor-pointer">
                    <span class="text-sm text-gray-600">Prikaži oblast</span>
                    <input type="checkbox" v-model="form.show_field" class="w-4 h-4 accent-violet-600"/>
                  </label>
                  <label class="flex items-center justify-between gap-3 cursor-pointer">
                    <span class="text-sm text-gray-600">Prikaži lokaciju</span>
                    <input type="checkbox" v-model="form.show_location" class="w-4 h-4 accent-violet-600"/>
                  </label>
                  <p class="text-xs text-gray-400 mt-1">🔒 Ime je uvijek javno vidljivo.</p>
                </div>
              </div>
            </div>

            <!-- Jezici + Vještine (dvije kolone unutar desne kolone) -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">

              <!-- Jezici -->
            <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
              <div class="flex items-center justify-between mb-5">
                  <div class="flex items-center gap-2">
                    <span class="text-violet-500">🌐</span>
                    <h3 class="text-sm font-semibold text-gray-800">Jezici</h3>
                  </div>
                  <button v-if="isEditMode" type="button" @click="form.languages.push({ name: '', level: '' })"
                    class="text-xs text-violet-600 hover:text-violet-800 font-medium">+ Dodaj</button>
                </div>
                <div v-if="form.languages.length === 0" class="text-sm text-gray-400 italic">Nije uneseno</div>
                <div v-for="(lang, i) in form.languages" :key="i" class="flex gap-2 mb-2 items-center">
                  <template v-if="isEditMode">
                    <input v-model="lang.name" type="text" placeholder="Npr. Engleski"
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                    <select v-model="lang.level"
                      class="w-28 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 bg-white text-gray-700">
                      <option value="" disabled>Nivo</option>
                      <option>A1</option>
                      <option>A2</option>
                      <option>B1</option>
                      <option>B2</option>
                      <option>C1</option>
                      <option>C2</option>
                    </select>
                    <button type="button" @click="form.languages.splice(i, 1)" class="text-red-400 hover:text-red-600 text-xs">✕</button>
                  </template>
                  <p v-else class="text-sm text-gray-700">{{ lang.name }} · <span class="text-gray-400">{{ lang.level }}</span></p>
                </div>
              </div>

              <!-- Vještine -->
              <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
                <div class="flex items-center justify-between mb-5">
                  <div class="flex items-center gap-2">
                    <span class="text-violet-500">🛠️</span>
                    <h3 class="text-sm font-semibold text-gray-800">Vještine</h3>
                  </div>
                  <button v-if="isEditMode" type="button" @click="form.skills.push('')"
                    class="text-xs text-violet-600 hover:text-violet-800 font-medium">+ Dodaj</button>
                </div>
                <div v-if="form.skills.length === 0" class="text-sm text-gray-400 italic">Nije uneseno</div>
                <div class="flex flex-wrap gap-2">
                  <div v-for="(skill, i) in form.skills" :key="i" class="flex items-center gap-1">
                    <template v-if="isEditMode">
                      <input v-model="form.skills[i]" type="text" placeholder="Npr. Python"
                        class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 w-28"/>
                      <button type="button" @click="form.skills.splice(i, 1)" class="text-red-400 hover:text-red-600 text-xs">✕</button>
                    </template>
                    <span v-else class="text-xs px-3 py-1.5 bg-violet-50 text-violet-700 border border-violet-100 rounded-full">{{ skill }}</span>
                  </div>
                </div>
              </div>

            </div>

          </div>
        </div>

        <!-- RED 2: Iskustvo + Obrazovanje -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 items-start">

          <!-- Iskustvo -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div class="flex items-center justify-between mb-5">
              <div class="flex items-center gap-2">
                <span class="text-violet-500">💼</span>
                <h3 class="text-sm font-semibold text-gray-800">Naučno i radno iskustvo</h3>
              </div>
              <button v-if="isEditMode" type="button"
                @click="form.experience.push({ title: '', organization: '', location: '', start_date: '', end_date: '', description: '' })"
                class="text-xs text-violet-600 hover:text-violet-800 font-medium">+ Dodaj</button>
            </div>
            <div v-if="form.experience.length === 0" class="text-sm text-gray-400 italic">Nije uneseno</div>
            <div v-for="(exp, i) in form.experience" :key="i" class="border border-gray-100 rounded-xl p-4 mb-3 last:mb-0">
              <template v-if="isEditMode">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-semibold text-gray-400 uppercase">Pozicija {{ i + 1 }}</span>
                  <button type="button" @click="form.experience.splice(i, 1)" class="text-red-400 hover:text-red-600 text-xs">Ukloni</button>
                </div>
                <div class="space-y-2">
                  <input v-model="exp.title" type="text" placeholder="Naziv pozicije"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  <input v-model="exp.organization" type="text" placeholder="Organizacija"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  <input v-model="exp.location" type="text" placeholder="Lokacija (opciono)"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  <div class="flex gap-2">
                    <input v-model="exp.start_date" type="text" placeholder="Od (npr. 2023-07)"
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                    <input v-model="exp.end_date" type="text" placeholder="Do (prazno = trenutno)"
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  </div>
                  <textarea v-model="exp.description" placeholder="Opis (opciono)" rows="2"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 resize-none"/>
                </div>
              </template>
              <template v-else>
                <div class="flex justify-between items-start gap-2 flex-wrap">
                  <p class="text-sm font-medium text-gray-800">{{ exp.title }}</p>
                  <span class="text-xs px-2 py-0.5 bg-violet-50 text-violet-600 rounded-full">{{ exp.start_date }} · {{ exp.end_date || 'Trenutno' }}</span>
                </div>
                <p class="text-xs text-violet-600 mt-0.5">{{ exp.organization }}</p>
                <p v-if="exp.location" class="text-xs text-gray-400 mt-0.5">📍 {{ exp.location }}</p>
                <p v-if="exp.description" class="text-xs text-gray-500 mt-1.5 leading-relaxed">{{ exp.description }}</p>
              </template>
            </div>
          </div>

          <!-- Obrazovanje -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-6">
            <div class="flex items-center justify-between mb-5">
              <div class="flex items-center gap-2">
                <span class="text-violet-500">🎓</span>
                <h3 class="text-sm font-semibold text-gray-800">Akademsko obrazovanje</h3>
              </div>
              <button v-if="isEditMode" type="button"
                @click="form.education.push({ degree: '', institution: '', start_date: '', end_date: '', description: '' })"
                class="text-xs text-violet-600 hover:text-violet-800 font-medium">+ Dodaj</button>
            </div>
            <div v-if="form.education.length === 0" class="text-sm text-gray-400 italic">Nije uneseno</div>
            <div v-for="(edu, i) in form.education" :key="i" class="border border-gray-100 rounded-xl p-4 mb-3 last:mb-0">
              <template v-if="isEditMode">
                <div class="flex justify-between items-center mb-2">
                  <span class="text-xs font-semibold text-gray-400 uppercase">Obrazovanje {{ i + 1 }}</span>
                  <button type="button" @click="form.education.splice(i, 1)" class="text-red-400 hover:text-red-600 text-xs">Ukloni</button>
                </div>
                <div class="space-y-2">
                  <input v-model="edu.degree" type="text" placeholder="Naziv studija / diplome"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  <input v-model="edu.institution" type="text" placeholder="Institucija"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  <div class="flex gap-2">
                    <input v-model="edu.start_date" type="text" placeholder="Od (npr. 2021-09)"
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                    <input v-model="edu.end_date" type="text" placeholder="Do (prazno = trenutno)"
                      class="flex-1 border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500"/>
                  </div>
                  <textarea v-model="edu.description" placeholder="Opis (opciono)" rows="2"
                    class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 resize-none"/>
                </div>
              </template>
              <template v-else>
                <div class="flex justify-between items-start gap-2 flex-wrap">
                  <p class="text-sm font-medium text-gray-800">{{ edu.degree }}</p>
                  <span class="text-xs px-2 py-0.5 bg-green-50 text-green-700 rounded-full">{{ edu.start_date }} · {{ edu.end_date || 'Trenutno' }}</span>
                </div>
                <p class="text-xs text-green-600 mt-0.5">{{ edu.institution }}</p>
                <p v-if="edu.description" class="text-xs text-gray-500 mt-1.5 leading-relaxed">{{ edu.description }}</p>
              </template>
            </div>
          </div>

        </div>

        <!-- Spremi/Odustani -->
        <div v-if="isEditMode" class="flex gap-3">
          <button type="submit" :disabled="!isFormValid"
            class="flex-1 bg-violet-600 text-white py-2.5 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed">
            Spremi promjene
          </button>
          <button type="button" @click="cancelEdit"
            class="flex-1 border border-gray-300 text-gray-600 py-2.5 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">
            Odustani
          </button>
        </div>

      </form>
    </div>

    <!-- Sigurnost tab -->
    <div v-if="activeTab === 'security'" class="flex justify-center">
      <div class="bg-white rounded-xl shadow-sm p-6 w-full max-w-lg min-h-96">
        <div v-if="passwordSuccess" class="bg-green-50 text-green-700 border border-green-200 rounded-lg px-4 py-3 mb-4 text-sm">{{ passwordSuccess }}</div>
        <div v-if="passwordError" class="bg-red-50 text-red-700 border border-red-200 rounded-lg px-4 py-3 mb-4 text-sm">{{ passwordError }}</div>
        <form @submit.prevent="changePassword" class="space-y-5">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Trenutna lozinka</label>
            <input v-model="passwordForm.old_password" type="password" placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Nova lozinka</label>
            <input v-model="passwordForm.new_password" type="password" placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"/>
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Potvrda nove lozinke</label>
            <input v-model="passwordForm.confirm_new_password" type="password" placeholder="••••••••"
              class="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-violet-500 focus:border-transparent"/>
          </div>
          <div class="pt-2">
            <button type="submit" :disabled="passwordLoading"
              class="w-full bg-violet-600 text-white py-2 px-4 rounded-lg text-sm font-medium hover:bg-violet-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed">
              {{ passwordLoading ? 'Spremanje...' : 'Promijeni lozinku' }}
            </button>
          </div>
          <div class="bg-red-50 border border-red-100 rounded-xl shadow-sm p-6 max-w-full mt-6">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-red-500">⚠️</span>
              <h3 class="text-sm font-semibold text-gray-800">Kontrola računa</h3>
            </div>
            <p class="text-sm text-red-400 mb-4">Deaktivacija će sakriti vaš profil iz javnog pretraživača.</p>
            <button @click="deactivateAccount"
              class="flex items-center gap-2 bg-red-500 hover:bg-red-600 text-white py-2 px-5 rounded-full text-sm font-medium transition-colors duration-200">
              🗑️ Deaktiviraj nalog
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- Modal deaktivacija -->
    <div v-if="showDeactivateModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-2xl shadow-xl p-6 max-w-sm w-full mx-4">
        <div class="flex items-center gap-2 mb-3">
          <span class="text-red-500 text-xl">⚠️</span>
          <h3 class="text-base font-semibold text-gray-800">Deaktivacija naloga</h3>
        </div>
        <p class="text-sm text-gray-500 mb-6">Jeste li sigurni da želite deaktivirati nalog? Vaš profil će biti sakriven, ali podaci neće biti obrisani.</p>
        <div class="flex gap-3">
          <button @click="closeDeactivateModal"
            class="flex-1 border border-gray-300 text-gray-700 py-2 px-4 rounded-lg text-sm font-medium hover:bg-gray-50 transition-colors">Odustani</button>
          <button @click="confirmDeactivation"
            class="flex-1 bg-red-500 hover:bg-red-600 text-white py-2 px-4 rounded-lg text-sm font-medium transition-colors">Potvrdi</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
import { updateProfile } from '../services/api.js'

export default {
  name: 'ProfileForm',

  props: {
    fullName: String,
    field: String,
    biography: String,
    avatarUrl: String,
    userRole: {
    type: String,
    default: 'member'
    },
    email: String,
    location: String,
    showBiography: { type: Boolean, default: true },
    showField: { type: Boolean, default: true },
    showLocation: { type: Boolean, default: true },
    languages: { type: Array, default: () => [] },
    experience: { type: Array, default: () => [] },
    education: { type: Array, default: () => [] },
    skills: { type: Array, default: () => [] },
    linkedinUrl: { type: String, default: '' },
    githubUrl: { type: String, default: '' },
    twitterUrl: { type: String, default: '' },

  },

  emits: ['profile-updated', 'avatar-uploaded', 'avatar-deleted'],

  data() {
  return {
    activeTab: 'info',
    isEditMode: false,
    passwordForm: {
      old_password: '',
      new_password: '',
      confirm_new_password: ''
    },
    passwordLoading: false,
    passwordSuccess: '',
    passwordError: '',
    form: {
      full_name: '',
      biography: '',
      field: '',
      location: '',
      email: '',
      show_biography: true,
      show_field: true,
      show_location: true,
      languages: [],
      experience: [],
      education: [],
      skills: [],
      linkedin_url: '',
      github_url: '',
      twitter_url: '',
    },
    errors: {
      full_name: '',
      biography: '',
      email: '',
    },
    successMessage: '',
    errorMessage: '',
    isUploading: false,
    avatarError: '', // <-- Dodan zarez ovdje

    fields: [ // <-- Promijenjeno u uglastu zagradu [
      'Softversko inženjerstvo',
      'Elektrotehnika',
      'Telekomunikacije',
      'Mašinstvo',
      'Arhitektura',
      'Biotehnologija',
      'Hemijsko inženjerstvo',
      'Građevinarstvo',
      'Fizika',
      'Matematika',
      'Medicina',
      'Farmacija',
      'Ekologija',
      'Ekonomija',
      'Dizajn' // Uklonjen zarez sa zadnjeg elementa (opcionalno, ali čistije)
    ], // <-- Promijenjeno u uglastu zagradu ]

    showDeactivateModal: false
  }
},

  computed: {
    isFormValid() {
      return (
        this.form.full_name && this.form.full_name.trim() !== '' &&
        (this.form.biography?.length || 0) <= 500
      )
    }
  },

watch: {
  // String fields
  fullName:    { immediate: true, handler(val) { this.form.full_name   = val || '' } },
  field:       { immediate: true, handler(val) { this.form.field       = val || '' } },
  biography:   { immediate: true, handler(val) { this.form.biography   = val || '' } },
  location:    { immediate: true, handler(val) { this.form.location    = val || '' } },
  email:       { immediate: true, handler(val) { this.form.email       = val || '' } },
  linkedinUrl: { immediate: true, handler(val) { this.form.linkedin_url = val || '' } },
  githubUrl:   { immediate: true, handler(val) { this.form.github_url   = val || '' } },
  twitterUrl:  { immediate: true, handler(val) { this.form.twitter_url  = val || '' } },

  // Array fields
  languages:  { immediate: true, handler(val) { this.form.languages  = val || [] } },
  experience: { immediate: true, handler(val) { this.form.experience = val || [] } },
  education:  { immediate: true, handler(val) { this.form.education  = val || [] } },
  skills:     { immediate: true, handler(val) { this.form.skills     = val || [] } },

  // Visibility toggles (only in create mode)
  showBiography: { immediate: true, handler(val) { if (!this.isEditMode) this.form.show_biography = val ?? true } },
  showField:     { immediate: true, handler(val) { if (!this.isEditMode) this.form.show_field     = val ?? true } },
  showLocation:  { immediate: true, handler(val) { if (!this.isEditMode) this.form.show_location  = val ?? true } },
},

  methods: {
  
    validateForm() {
      this.errors = { full_name: '', biography: '' }
      let isValid = true
      if (!this.form.full_name || this.form.full_name.trim() === '') {
        this.errors.full_name = 'Ime ne smije biti prazno.'
        isValid = false
      }
      if (this.form.biography && this.form.biography.length > 500) {
        this.errors.biography = 'Biografija ne smije biti duža od 500 karaktera.'
        isValid = false
      }
      if (this.form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(this.form.email)) {
        this.errors.email = 'Email adresa nije ispravna.'
        isValid = false
      }
      return isValid
    },

   async saveProfile() {
  if (!this.validateForm()) return
  this.successMessage = ''
  this.errorMessage = ''

  try {
    const token = localStorage.getItem('token')
    const payload = {
      full_name: this.form.full_name,
      biography: this.form.biography,
      field: this.form.field,
      location: this.form.location,
      email: this.form.email,
      show_biography: this.form.show_biography,
      show_field: this.form.show_field,
      show_location: this.form.show_location,
      languages:    this.form.languages,
      experience:   this.form.experience,
      education:    this.form.education,
      skills:       this.form.skills,
      linkedin_url: this.form.linkedin_url,
      github_url:   this.form.github_url,
      twitter_url:  this.form.twitter_url,
    }
    console.log('Payload koji se šalje:', JSON.stringify(payload))
    await updateProfile(token, payload)
    this.successMessage = 'Promjene su uspješno sačuvane!'
    this.isEditMode = false
    this.$emit('profile-updated', this.form)
    setTimeout(() => { this.successMessage = '' }, 3000)
  } catch (error) {
    this.errorMessage = 'Greška pri čuvanju. Pokušajte ponovo.'
    setTimeout(() => { this.errorMessage = '' }, 3000)
  }
},

        cancelEdit() {
      this.isEditMode = false
      // Resetuj formu na originalne vrijednosti
      this.form.full_name = this.fullName || ''
      this.form.field = this.field || ''
      this.form.biography = this.biography || ''
      this.errors = { full_name: '', biography: '' }
      this.form.show_biography = this.showBiography
      this.form.show_field = this.showField
      this.form.show_location = this.showLocation
      this.form.languages    = this.languages   || []
      this.form.experience   = this.experience  || []
      this.form.education    = this.education   || []
      this.form.skills       = this.skills      || []
      this.form.linkedin_url = this.linkedinUrl || ''
      this.form.github_url   = this.githubUrl   || ''
      this.form.twitter_url  = this.twitterUrl  || ''
    },

    async handleAvatarChange(event) {
      const file = event.target.files[0]
      if (!file) return

      this.isUploading = true
      this.avatarError = ''

      const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png']
      if (!allowedTypes.includes(file.type)) {
        this.avatarError = 'Neispravan format! Dozvoljeni su samo JPG i PNG.'
        this.isUploading = false
        event.target.value = ''
        return
      }

      const maxSizeInBytes = 2 * 1024 * 1024
      if (file.size > maxSizeInBytes) {
        this.avatarError = 'Slika je prevelika! Maksimalna veličina je 2MB.'
        this.isUploading = false
        event.target.value = ''
        return
      }

      try {
        const token = localStorage.getItem('token')
        const formData = new FormData()
        formData.append('file', file)

        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail)
        }

        const data = await response.json()
        this.$emit('avatar-uploaded', `http://localhost:8000${data.avatar_url}`)

      } catch (error) {
        this.avatarError = error.message || 'Greška pri uploadu slike.'
      } finally {
        this.isUploading = false
        event.target.value = ''
      }
    },

    async changePassword() {
      this.passwordSuccess = ''
      this.passwordError = ''

      if (!this.passwordForm.old_password || !this.passwordForm.new_password || !this.passwordForm.confirm_new_password) {
        this.passwordError = 'Sva polja su obavezna.'
        return
      }

      if (this.passwordForm.new_password !== this.passwordForm.confirm_new_password) {
        this.passwordError = 'Nova lozinka i potvrda se ne poklapaju.'
        return
      }

      if (this.passwordForm.new_password.length < 8) {
        this.passwordError = 'Nova lozinka mora imati najmanje 8 karaktera.'
        return
      }

      try {
        this.passwordLoading = true
        const token = localStorage.getItem('token')

        const response = await fetch('http://localhost:8000/profiles/me/change-password', {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify(this.passwordForm)
        })

        const data = await response.json()

        if (response.ok) {
          this.passwordSuccess = data.message || 'Lozinka uspješno promijenjena.'
          this.passwordForm = { old_password: '', new_password: '', confirm_new_password: '' }
          setTimeout(() => { this.passwordSuccess = '' }, 3000)
        } else {
          this.passwordError = data.detail || 'Greška pri promjeni lozinke.'
        }
      } catch (e) {
        this.passwordError = 'Backend ne radi.'
      } finally {
        this.passwordLoading = false
      }
    },

    async handleDeleteAvatar() {
      if (!confirm('Jeste li sigurni da želite obrisati profilnu sliku?')) return

      this.avatarError = ''
      try {
        const token = localStorage.getItem('token')
        const response = await fetch('http://localhost:8000/profiles/me/avatar', {
          method: 'DELETE',
          headers: { 'Authorization': `Bearer ${token}` }
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Greška pri brisanju.')
        }

        this.$emit('avatar-deleted')
      } catch (error) {
        this.avatarError = error.message || 'Nije moguće obrisati profilnu sliku.'
      }
    },
    deactivateAccount() {
  this.showDeactivateModal = true
},

closeDeactivateModal() {
  this.showDeactivateModal = false
},

async confirmDeactivation() {
  try {
    const token = localStorage.getItem('token')
    const response = await fetch('http://localhost:8000/profiles/me/deactivate', {
      method: 'PATCH',
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (response.ok) {
      this.showDeactivateModal = false
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  } catch (e) {
    console.error('Greška pri deaktivaciji.')
  }
},
  }
}
</script>