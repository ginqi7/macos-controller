;;; macos-controller.el --- MacOS Controller.        -*- lexical-binding: t; -*-

;; Copyright (C) 2023  Qiqi Jin

;; Author: Qiqi Jin <ginqi7@gmail.com>
;; This program is free software; you can redistribute it and/or modify
;; it under the terms of the GNU General Public License as published by
;; the Free Software Foundation, either version 3 of the License, or
;; (at your option) any later version.

;; This program is distributed in the hope that it will be useful,
;; but WITHOUT ANY WARRANTY; without even the implied warranty of
;; MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
;; GNU General Public License for more details.

;; You should have received a copy of the GNU General Public License
;; along with this program.  If not, see <https://www.gnu.org/licenses/>.

;;; Commentary:

;;

;;; Installation:
;; Manual:
;; Download the source code and put it wherever you like, e.g. into
;; ~/.emacs.d/macos-controller/
;; ```
;; git clone git@github.com:ginqi7/macos-controller.git
;; ```
;; Add the downloaded directory to the load path:
;; ```
;; (add-to-list 'load-path "~/.emacs.d/macos-controller/")
;; (require 'macos-controller)
;; ```
;;

;;; Code:

(defvar macc--last-actived-app nil)

(defcustom macc-py-executor "python"
  "Python executor."
  :group 'macos-controller
  :type '(string)
  )

(defvar macc-py-path
  (concat
   (file-name-directory
    (if load-file-name load-file-name (buffer-file-name)))
   "macos-controller.py"))

(defun macc--run-command (parameters)
  "Run python program with PARAMETERS."
  (string-trim
   (shell-command-to-string
    (string-join
     (append (list macc-py-executor macc-py-path) parameters)
     " "))))

(defun macc-get-actived-app ()
  "Get actived app name."
  (setq macc--last-actived-app (macc--run-command '("get_actived_app"))))

(defun macc-app-switch-to-last-actived-app ()
  "Swith to last actived app."
  (when macc--last-actived-app
    (macc-app-switch-to macc--last-actived-app)))

(defun macc-app-switch-to (app-name)
  "Swith to APP-NAME."
  (macc--run-command (list "switch_to" app-name)))

(defun macc-list-all-running-apps ()
  "List all running apps."
  (read (macc--run-command (list "list_all_running_apps"))))

(defun macc-kill-app (name)
  "Kill running app by NAME."
  (macc--run-command (list "kill_app" name)))

(provide 'macos-controller)
;;; macos-controller.el ends here
