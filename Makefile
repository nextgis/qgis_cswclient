UNAME := $(shell uname)

ifeq ($(UNAME), MINGW32_NT-6.1)
PYUIC4=cmd //c pyuic4
PYRCC4=cmd //c pyrcc4
PYLUPDATE4=cmd //c pylupdate4
else
PYUIC4=pyuic4
PYRCC4=pyrcc4
PYLUPDATE4=pylupdate4
endif

UI_PATH=ui
UI_SOURCES=$(wildcard $(UI_PATH)/*.ui)
UI_FILES=$(patsubst $(UI_PATH)/%.ui, $(UI_PATH)/ui_%.py, $(UI_SOURCES))

LANG_PATH=i18n
LANG_SOURCES=$(wildcard $(LANG_PATH)/*.ts)
LANG_FILES=$(patsubst $(LANG_PATH)/%.ts, $(LANG_PATH)/%.qm, $(LANG_SOURCES))

RES_PATH=.
RES_SOURCES=$(wildcard $(RES_PATH)/*.qrc)
RES_FILES=$(patsubst $(RES_PATH)/%.qrc, $(RES_PATH)/%_rc.py, $(RES_SOURCES))

PRO_PATH=.
PRO_FILES=$(wildcard $(PRO_PATH)/*.pro)

ALL_FILES= ${RES_FILES} ${UI_FILES} ${LANG_FILES}

all: $(ALL_FILES)

ui: $(UI_FILES)

ts: $(PRO_FILES)
	$(PYLUPDATE4) -verbose $<

lang: $(LANG_FILES)

res: $(RES_FILES)

$(UI_FILES): $(UI_PATH)/ui_%.py: $(UI_PATH)/%.ui
	$(PYUIC4) -o $@ $<

$(LANG_FILES): $(LANG_PATH)/%.qm: $(LANG_PATH)/%.ts
	lrelease $<

$(RES_FILES): $(RES_PATH)/%_rc.py: $(RES_PATH)/%.qrc
	$(PYRCC4) -o $@ $<

clean:
	rm -f $(ALL_FILES)
	find -name "*.pyc" -exec rm -f {} \;
	rm -f *.zip

package:
	cd .. && rm -f *.zip && zip -r metasearch.zip metasearch -x \*.pyc \*.ui \*.qrc \*.pro \*~ \*.git\* \*Makefile*
	mv ../metasearch.zip .

upload:
	plugin_uploader.py metasearch.zip
