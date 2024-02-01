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


(require 'websocket-bridge)

(defvar macc--last-actived-app nil)

(defvar macos-controller-py-path
  (concat
   (if load-file-name
       (file-name-directory load-file-name)
     (file-name-directory (buffer-file-name)))
   "macos-controller.py"))

(defun macos-controller-start ()
  "Start websocket bridge real-time-translation."
  (interactive)
  (websocket-bridge-app-start "macos-controller" (executable-find "python3") macos-controller-py-path))

(defun macos-controller-restart ()
  "Restart websocket bridge real-time-translation and show process."
  (interactive)
  (websocket-bridge-app-exit "macos-controller")
  (macos-controller-start)
  (websocket-bridge-app-open-buffer "macos-controller"))


(defun macc-get-actived-app ()
  "Get actived app name."
  (websocket-bridge-call "macos-controller" "get_actived_app"))


(defun macc-app-switch-to-last-actived-app ()
  "Swith to last actived app."
  (when macc--last-actived-app
    (macc-app-switch-to macc--last-actived-app)))

(defun macc-app-switch-to (app-name)
  "Swith to APP-NAME."
  (websocket-bridge-call "macos-controller" "switch_to" app-name))

(defun macc-list-all-running-apps ()
  "List all running apps."
  (websocket-bridge-call "macos-controller" "list_all_running_apps"))

(defun macc-paste ()
  "Paste."
  (websocket-bridge-call "macos-controller" "paste"))

(defun macc-press (key)
  "Press KEY."
  (websocket-bridge-call "macos-controller" "press" key))

(defun macc-command-tab ()
  "Press KEY."
  (websocket-bridge-call "macos-controller" "command_tab"))

(defun macc-kill-app (name)
  "Kill running app by NAME."
  (macc--run-command (list "kill_app" name)))

(defun macc-mouse-position ()
  "Get mouse position."
  (let ((mouse-position
         (read (macc--run-command (list "mouse_position")))))
    (cons (car mouse-position) (nth 1 mouse-position))))

(provide 'macos-controller)
;;; macos-controller.el ends here
