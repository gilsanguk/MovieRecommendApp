<template>
  <div class="bgdiv">
    <div class="bgdivdiv">
      <h1 class="text-truncate m-3 pb-3 text-white"><b>비슷한 영화를 추천해드릴게요!</b></h1>
      <div id="searchdiv">
        <autocomplete
          :search="search"
          placeholder="Search for a movie"
          aria-label="Search for a movie"
          :get-result-value="getResultValue"
          @submit="onSubmit"
        >
          <template #result="{ result, props }">
            <li class="result-li" v-bind="props">
              <div class="result">
                <img :src="result.poster_path" />
                <span class="result-title text-truncate">{{
                  result.title
                }}</span>
              </div>
            </li>
          </template>
        </autocomplete>
      </div>
      <!-- 장바구니 -->
      <h2 class="m-3 p-3 text-white">선택한 영화 <span class="number">({{ selectmovies.length }}/6)</span>
         <button @click="resetPrefer" id="clickbutton">추천받기</button>
      </h2>
      <div class="row row-cols-1 row-cols-sm-2 row-cols-md-3 g-4">
        <div class="centered col" v-for="i in 6" :key="i">
          <SelectedMovieItem :movie="selectmovies[i-1]" @delete-movie="deleteMovie" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Swal from 'sweetalert2/dist/sweetalert2'
import Autocomplete from "@trevoreyre/autocomplete-vue";
import SelectedMovieItem from "@/components/SelectedMovieItem";

export default {
  name: "SelectMovieView",
  data() {
    return {
      selectmovies: [],
    };
  },
  components: {
    Autocomplete,
    SelectedMovieItem,
  },
  methods: {
    // 검색
    search(input) {
      if (input.length < 1) {
        return [];
      }
      return this.movies.filter((movie) => {
        return (
          (movie.title.toLowerCase().startsWith(input.toLowerCase()) ||
            movie.title.toLowerCase().includes(input.toLowerCase())) &&
          !this.selectmovies.includes(movie)
        );
      });
    },
    getResultValue() {
      return "";
    },
    // 삭제
    deleteMovie(movie) {
      this.selectmovies = this.selectmovies.filter((m) => m.id !== movie.id);
    },
    // 영화 추천
    onSubmit(result) {
      if (this.selectmovies.length < 6) {
        this.selectmovies.push(result);
      } else {
        Swal.fire({
          position: 'center',
          icon: 'warning',
          title: '6개까지만 선택 가능합니다.',
        })
      }
    },
    resetPrefer() {
      if (this.selectmovies.length == 0) {
        Swal.fire({
          position: 'center',
          icon: 'warning',
          title: '영화를 선택해주세요.',
        })
      } else {
        this.$store.dispatch("resetPrefer", this.selectmovies)
      }
    },
  },
  computed: {
    movies() {
      return this.$store.getters.all;
    },
  },
  created() {
    this.$store.dispatch("getAllMovies");
    this.$modal.hideAll()
  },
};
</script>

<style scoped>
/* 기본 */
.centered {
  display: flex !important;
  justify-content: center !important;
  align-items: center !important;
}

.bgdiv {
  min-height: 100vh;
  padding: 2rem 5rem;
}

.bgdivdiv {
  margin: 0% 15%;
}

#searchdiv {
  margin: 0 auto;
  font-size: 40px;
}

/* 검색목록 */
.result {
  display: flex;
  align-items: center;
  color: black;
}

.result img {
  min-width: 40px;
  width: 5%;
  height: 5%;
  margin-right: 20px;
}

.result-title {
  font-size: 1rem;
}

/* 선택한 영화 */
#selecteddiv {
  margin-top: 2rem;
  margin-bottom: 2rem;
}

#selecteddiv div {
  margin: 2rem 1rem;
}

/*  버튼 */
#clickbutton {
  color: #a7a7a7;
  background-color: #141619;
  border: 0;
  outline: none;
  margin-left: 1rem;
}

#clickbutton:hover {
  color: white;
  transition: 0.4s;
}
</style>