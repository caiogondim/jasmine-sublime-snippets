/* global module */
module.exports = function(grunt) {
  "use strict";

  grunt.loadNpmTasks("grunt-lintspaces")
  grunt.loadNpmTasks("grunt-bump")

  grunt.initConfig({
    lintspaces: {
      all: {
        src: ["*"],
        options: {
          editorconfig: ".editorconfig"
        }
      }
    },
    bump: {
      options: {
        pushTo: "origin",
        tagName: "%VERSION%"
      }
    }
  })

  grunt.registerTask("test", ["lintspaces"])
}
