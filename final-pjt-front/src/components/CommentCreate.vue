<template>
  <div id="commentform" class="py-2">
    <!-- 리뷰 작성 폼 -->
    <form @submit.prevent>
      <div id="content">
        <p class="my-2">댓글</p>
        <textarea
          class="form-control"
          rows="3"
          placeholder="내용을 입력해 주세요"
          v-model.trim="content"
        ></textarea>
      </div>
      <button
        type="submit"
        id="summitbtn"
        @click="comment ? updateComment() : createComment()"
        :class="content !== '' ? 'focus' : ''"
      >
        작성
      </button>
    </form>
  </div>
</template>

<script>
import axios from "axios";
import Swal from "sweetalert2";

const API_URL = "http://127.0.0.1:8000/moji";

export default {
  name: "CommentsCreate",
  props: {
    reviewId: Number,
    comment: Object,
  },
  data() {
    return {
      content: "",
    };
  },
  methods: {
    // 댓글 생성 요청
    createComment() {
      if (!this.content) {
        Swal.fire({
          position: "center",
          icon: "warning",
          title: "내용을 입력해주세요",
        });
      }
      const data = {
        content: this.content,
      };
      axios({
        method: "post",
        url: `${API_URL}/community/reviews/${this.reviewId}/comments/create/`,
        headers: { Authorization: `Token ${this.$store.getters.getToken}` },
        data: data,
      })
        .then(() => {
          this.content = "";
          this.$emit("get-comments");
        })
        .catch((err) => {
          if (err.response.status === 401) {
            this.$router.push({ name: "LoginView" });
          } else if (err.response.status === 404) {
            this.$router.push({ name: "NotFound404" });
          } else {
            console.log(err);
          }
        });
    },
    // 댓글 수정
    updateComment() {
      if (!this.content) {
        Swal.fire({
          position: "center",
          icon: "warning",
          title: "내용을 입력해주세요",
        });
      }
      const data = {
        content: this.content,
      };
      axios({
        method: "put",
        url: `${API_URL}/community/reviews/${this.$route.params.reviewId}/comments/${this.comment.id}/`,
        headers: { Authorization: `Token ${this.$store.getters.getToken}` },
        data: data,
      }).then(() => {
        this.content = "";
        this.$emit("get-comments");
      });
    },
  },
  created() {
    if (this.comment) {
      this.content = this.comment.content;
    }
  },
};
</script>

<style scoped>
/* 기본 */
.vm--modal {
  border-radius: 10px;
  overflow-y: scroll;
  background-color: #292929;
}

#commentform {
  position: relative;
}

#closebtn {
  float: right;
  background-color: transparent;
  font-size: xx-large;
  color: #a7a7a7;
  border: 0;
  outline: 0;
}

#content p {
  color: white;
  font-size: large;
  font-weight: bold;
  text-align: start;
}

#content .form-control {
  resize: none;
}

#summitbtn {
  font-size: small;
  padding: 1.5% 2%;
  position: absolute;
  bottom: 8%;
  right: 2%;
  border-radius: 10px;
}

.focus {
  background-color: rgb(255, 190, 134);
  color: black;
}

button:hover {
  color: #a7a7a7 !important;
}
</style>