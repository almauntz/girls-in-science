<template>
  <div class="admin-page">

    <!-- ── Naslov stranice ── -->
    <div class="page-header">
      <span class="admin-tag">Admin panel</span>
      <h1>Upravljanje radionicama</h1>
      <p class="page-sub">Odaberi akciju koju želiš izvršiti</p>
    </div>

    <!-- ── Tri kartice (glavni ekran) ── -->
    <div class="actions-row">

      <!-- Kartica 1: Kreiraj -->
      <button class="action-card card-create" @click="openModal('create')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="10"/>
            <line x1="12" y1="8" x2="12" y2="16"/>
            <line x1="8" y1="12" x2="16" y2="12"/>
          </svg>
        </div>
        <span class="card-label">Kreiraj radionicu</span>
        <span class="card-hint">Dodaj novu radionicu na platformu</span>
      </button>

      <!-- Kartica 2: Uredi -->
      <button class="action-card card-edit" @click="openModal('edit')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/>
            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/>
          </svg>
        </div>
        <span class="card-label">Uredi radionicu</span>
        <span class="card-hint">Izmijeni podatke postojeće radionice</span>
      </button>

      <!-- Kartica 3: Obriši -->
      <button class="action-card card-delete" @click="openModal('delete')">
        <div class="card-icon">
          <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <polyline points="3 6 5 6 21 6"/>
            <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/>
            <path d="M10 11v6"/><path d="M14 11v6"/>
            <path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/>
          </svg>
        </div>
        <span class="card-label">Obriši radionicu</span>
        <span class="card-hint">Trajno ukloni radionicu iz sistema</span>
      </button>

    </div>
</div>

</template>