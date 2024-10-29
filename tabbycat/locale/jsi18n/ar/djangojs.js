

'use strict';
{
  const globals = this;
  const django = globals.django || (globals.django = {});

  
  django.pluralidx = function(count) { return (count == 1) ? 0 : 1; };
  

  /* gettext library */

  django.catalog = django.catalog || {};
  
  const newcatalog = {
    "%(sel)s of %(cnt)s selected": [
      "\u0644\u0627 \u0634\u064a \u0645\u062d\u062f\u062f",
      "%(sel)s \u0645\u0646 %(cnt)s \u0645\u062d\u062f\u062f"
    ],
    "6 a.m.": "6 \u0635.",
    "6 p.m.": "6 \u0645\u0633\u0627\u0621\u064b",
    "Add": "\u0623\u0636\u0641",
    "Adjudicator Demographics": "\u062a\u0648\u0632\u064a\u0639 \u0627\u0644\u062d\u0643\u0627\u0645 ",
    "Adjudicator Results": "\u0646\u062a\u0627\u0626\u062c \u0627\u0644\u062d\u0643\u0645 ",
    "All": "\u0627\u0644\u0643\u0644",
    "April": "\u0623\u0628\u0631\u064a\u0644",
    "August": "\u0623\u063a\u0633\u0637\u0633",
    "Available %s": "%s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629",
    "Break": "\u062a\u0623\u0647\u0644 ",
    "Cancel": "\u0625\u0644\u063a\u0627\u0621",
    "Category": "\u0627\u0644\u0641\u0626\u0629",
    "Choose": "\u0627\u062e\u062a\u064a\u0627\u0631",
    "Choose a Date": "\u0625\u062e\u062a\u0631 \u062a\u0627\u0631\u064a\u062e ",
    "Choose a Time": "\u0625\u062e\u062a\u0631 \u0648\u0642\u062a",
    "Choose a time": "\u0627\u062e\u062a\u0631 \u0648\u0642\u062a\u0627\u064b",
    "Choose all": "\u0627\u062e\u062a\u0631 \u0627\u0644\u0643\u0644",
    "Chosen %s": "%s \u0627\u0644\u0645\u064f\u062e\u062a\u0627\u0631\u0629",
    "Click to choose all %s at once.": "\u0627\u0636\u063a\u0637 \u0644\u0627\u062e\u062a\u064a\u0627\u0631 \u062c\u0645\u064a\u0639 %s \u062c\u0645\u0644\u0629 \u0648\u0627\u062d\u062f\u0629.",
    "Click to remove all chosen %s at once.": "\u0627\u0636\u063a\u0637 \u0644\u0625\u0632\u0627\u0644\u0629 \u062c\u0645\u064a\u0639 %s \u0627\u0644\u0645\u062d\u062f\u062f\u0629 \u062c\u0645\u0644\u0629 \u0648\u0627\u062d\u062f\u0629.",
    "Confirmed": "\u0645\u0639\u062a\u0645\u062f",
    "Copy From Check-Ins": "\u0646\u0633\u062e\u0629 \u0645\u0646 \u062a\u0633\u062c\u064a\u0644 \u0627\u0644\u062f\u062e\u0648\u0644 ",
    "December": "\u062f\u064a\u0633\u0645\u0628\u0631",
    "Delete": "\u062d\u0630\u0641",
    "February": "\u0641\u0628\u0631\u0627\u064a\u0631",
    "Filter": "\u062a\u0635\u0641\u064a\u0629",
    "Find in Table": "\u0627\u0644\u0628\u062d\u062b \u0641\u064a \u0627\u0644\u062c\u062f\u0648\u0644",
    "General": "\u0639\u0627\u0645",
    "Hide": "\u0627\u062e\u0641",
    "January": "\u064a\u0646\u0627\u064a\u0631",
    "July": "\u064a\u0648\u0644\u064a\u0648",
    "June": "\u064a\u0648\u0646\u064a\u0648",
    "March": "\u0645\u0627\u0631\u0633",
    "Match": "\u062a\u0648\u0627\u0641\u0642",
    "Match Check-Ins": "\u062a\u0634\u0627\u0628\u0647 \u0627\u0644\u0625\u062f\u062e\u0627\u0644 ",
    "May": "\u0645\u0627\u064a\u0648",
    "Midnight": "\u0645\u0646\u062a\u0635\u0641 \u0627\u0644\u0644\u064a\u0644",
    "No": "\u0644\u0627",
    "No Adjudicator Ratings Information": "\u0644\u0627 \u062a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u062d\u0648\u0644 \u062a\u0635\u0646\u064a\u0641 \u0627\u0644\u062d\u0643\u0627\u0645",
    "No Adjudicator-Adjudicator Feedback Information": "\u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0639\u0646 \u0627\u0644\u062a\u063a\u0630\u064a\u0629 \u0627\u0644\u0631\u0627\u062c\u0639\u0629 \u062d\u0648\u0644 \u062a\u062d\u0643\u064a\u0645 \u0627\u0644\u0645\u062d\u0643\u0645\u064a\u0646 ",
    "No Gender Information": "\u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0627\u0644\u062c\u0646\u0633",
    "No Position Information": "\u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0639\u0646 \u0627\u0644\u0648\u0638\u064a\u0641\u0629 ",
    "No Region Information": "\u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0639\u0646 \u0627\u0644\u0645\u0646\u0637\u0642\u0629 ",
    "No Speaker Categories Information": "\u0644\u0627 \u064a\u0648\u062c\u062f \u0645\u0639\u0644\u0648\u0645\u0627\u062a \u0639\u0646 \u0641\u0626\u0629 \u0627\u0644\u0645\u062a\u062d\u062f\u062b ",
    "Noon": "\u0627\u0644\u0638\u0647\u0631",
    "Note: You are %s hour ahead of server time.": [
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0642\u062f\u0645 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645."
    ],
    "Note: You are %s hour behind server time.": [
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645.",
      "\u0645\u0644\u0627\u062d\u0638\u0629: \u0623\u0646\u062a \u0645\u062a\u0623\u062e\u0631 \u0628\u0640 %s \u0633\u0627\u0639\u0629 \u0645\u0646 \u0648\u0642\u062a \u0627\u0644\u062e\u0627\u062f\u0645."
    ],
    "November": "\u0646\u0648\u0641\u0645\u0628\u0631",
    "Now": "\u0627\u0644\u0622\u0646",
    "October": "\u0623\u0643\u062a\u0648\u0628\u0631",
    "Rank": "\u0627\u0644\u0645\u0633\u062a\u0648\u0649",
    "Remove": "\u0627\u062d\u0630\u0641",
    "Remove all": "\u0625\u0632\u0627\u0644\u0629 \u0627\u0644\u0643\u0644",
    "September": "\u0633\u0628\u062a\u0645\u0628\u0631",
    "Set All Breaking as Available": "\u0648\u0636\u0639 \u062c\u0645\u064a\u0639 \u0627\u0644\u0645\u062a\u0623\u0647\u0644\u064a\u0646 \"\u0645\u062a\u0648\u0627\u062c\u062f\u0648\u0646\"",
    "Set all the availabilities to exactly match what they were in the previous round.": "\u062a\u0639\u064a\u064a\u0646 \u062c\u0645\u064a\u0639 \u0627\u0644\u0623\u0634\u064a\u0627\u0621 \u0644\u0644\u062a\u062a\u0648\u0627\u0641\u0642 \u0645\u0639 \u062a\u0644\u0643 \u0627\u0644\u0645\u062a\u0627\u062d\u0629 \u0641\u064a \u0627\u0644\u062c\u0648\u0644\u0629 \u0627\u0644\u0633\u0627\u0628\u0642\u0629.",
    "Set people as available only if they have a check-in and are currently unavailable \u2014 i.e. it will not overwrite any existing availabilities.": "\u062a\u0639\u064a\u064a\u0646 \u0627\u0644\u0623\u0634\u062e\u0627\u0635 \u0639\u0644\u0649 \u0623\u0646\u0647\u0627 \u0645\u062a\u0648\u0641\u0631\u0629 \u0641\u0642\u0637 \u0625\u0630\u0627 \u0643\u0627\u0646 \u0644\u062f\u064a\u0647\u0645 \u062a\u0633\u062c\u064a\u0644 \u062f\u062e\u0648\u0644 \u0648 \u063a\u064a\u0631 \u0645\u062a\u0627\u062d\u0648\u0646 \u062d\u0627\u0644\u064a\u064b\u0627 \u2014 \u0628\u0645\u0639\u0646\u0649 \u0623\u0646\u0647 \u0644\u0646 \u064a\u0624\u062f\u064a \u0625\u0644\u0649 \u0627\u0633\u062a\u0628\u062f\u0627\u0644 \u0623\u064a \u0645\u0646 \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u064a\u0646 \u062d\u0627\u0644\u064a\u0627.",
    "Show": "\u0623\u0638\u0647\u0631",
    "Speaker Demographics": "\u062a\u0648\u0632\u064a\u0639 \u0627\u0644\u0645\u062a\u062d\u062f\u062b\u064a\u0646 ",
    "Speaker Results": "\u0646\u062a\u0627\u0626\u062c \u0627\u0644\u0645\u062a\u062d\u062f\u062b ",
    "Team": "\u0641\u0631\u064a\u0642",
    "This is the list of available %s. You may choose some by selecting them in the box below and then clicking the \"Choose\" arrow between the two boxes.": "\u0647\u0630\u0647 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629. \u064a\u0645\u0643\u0646\u0643 \u0627\u062e\u062a\u064a\u0627\u0631 \u0628\u0639\u0636\u0647\u0627 \u0628\u0627\u0646\u062a\u0642\u0627\u0626\u0647\u0627 \u0641\u064a \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0623\u062f\u0646\u0627\u0647 \u062b\u0645 \u0627\u0644\u0636\u063a\u0637 \u0639\u0644\u0649 \u0633\u0647\u0645 \u0627\u0644\u0640\"\u0627\u062e\u062a\u064a\u0627\u0631\" \u0628\u064a\u0646 \u0627\u0644\u0635\u0646\u062f\u0648\u0642\u064a\u0646.",
    "This is the list of chosen %s. You may remove some by selecting them in the box below and then clicking the \"Remove\" arrow between the two boxes.": "\u0647\u0630\u0647 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062d\u062f\u062f\u0629. \u064a\u0645\u0643\u0646\u0643 \u0625\u0632\u0627\u0644\u0629 \u0628\u0639\u0636\u0647\u0627 \u0628\u0627\u062e\u062a\u064a\u0627\u0631\u0647\u0627 \u0641\u064a \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0623\u062f\u0646\u0627\u0647 \u062b\u0645 \u0627\u0636\u063a\u0637 \u0639\u0644\u0649 \u0633\u0647\u0645 \u0627\u0644\u0640\"\u0625\u0632\u0627\u0644\u0629\" \u0628\u064a\u0646 \u0627\u0644\u0635\u0646\u062f\u0648\u0642\u064a\u0646.",
    "Today": "\u0627\u0644\u064a\u0648\u0645",
    "Tomorrow": "\u063a\u062f\u0627\u064b",
    "Type into this box to filter down the list of available %s.": "\u0627\u0643\u062a\u0628 \u0641\u064a \u0647\u0630\u0627 \u0627\u0644\u0635\u0646\u062f\u0648\u0642 \u0644\u062a\u0635\u0641\u064a\u0629 \u0642\u0627\u0626\u0645\u0629 %s \u0627\u0644\u0645\u062a\u0648\u0641\u0631\u0629.",
    "Unaffiliated": "\u063a\u064a\u0631 \u0645\u0646\u062a\u0633\u0628\u064a\u0646",
    "Unknown": "\u0645\u062c\u0647\u0648\u0644 ",
    "Warning: you have unsaved changes": "\u062a\u062d\u0630\u064a\u0631: \u0644\u062f\u064a\u0643 \u062a\u063a\u064a\u0631\u0627\u062a \u063a\u064a\u0631 \u0645\u062d\u0641\u0648\u0638\u0629",
    "Yes": "\u0646\u0639\u0645 ",
    "Yesterday": "\u0623\u0645\u0633",
    "You have selected an action, and you haven\u2019t made any changes on individual fields. You\u2019re probably looking for the Go button rather than the Save button.": "\u0644\u0642\u062f \u062d\u062f\u062f\u062a \u0625\u062c\u0631\u0627\u0621 \u060c \u0648\u0644\u0645 \u062a\u0642\u0645 \u0628\u0625\u062c\u0631\u0627\u0621 \u0623\u064a \u062a\u063a\u064a\u064a\u0631\u0627\u062a \u0639\u0644\u0649 \u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0641\u0631\u062f\u064a\u0629. \u0645\u0646 \u0627\u0644\u0645\u062d\u062a\u0645\u0644 \u0623\u0646\u0643 \u062a\u0628\u062d\u062b \u0639\u0646 \u0627\u0644\u0632\u0631 \u0623\u0630\u0647\u0628 \u0628\u062f\u0644\u0627\u064b \u0645\u0646 \u0627\u0644\u0632\u0631 \u062d\u0641\u0638.",
    "You have selected an action, but you haven\u2019t saved your changes to individual fields yet. Please click OK to save. You\u2019ll need to re-run the action.": "\u0644\u0642\u062f \u062d\u062f\u062f\u062a \u0625\u062c\u0631\u0627\u0621\u064b \u060c \u0644\u0643\u0646\u0643 \u0644\u0645 \u062a\u062d\u0641\u0638 \u062a\u063a\u064a\u064a\u0631\u0627\u062a\u0643 \u0641\u064a \u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0641\u0631\u062f\u064a\u0629 \u062d\u062a\u0649 \u0627\u0644\u0622\u0646. \u064a\u0631\u062c\u0649 \u0627\u0644\u0646\u0642\u0631 \u0641\u0648\u0642 \u0645\u0648\u0627\u0641\u0642 \u0644\u0644\u062d\u0641\u0638. \u0633\u062a\u062d\u062a\u0627\u062c \u0625\u0644\u0649 \u0625\u0639\u0627\u062f\u0629 \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0625\u062c\u0631\u0627\u0621.",
    "You have unsaved changes on individual editable fields. If you run an action, your unsaved changes will be lost.": "\u0644\u062f\u064a\u0643 \u062a\u0639\u062f\u064a\u0644\u0627\u062a \u063a\u064a\u0631 \u0645\u062d\u0641\u0648\u0638\u0629 \u0639\u0644\u0649 \u0628\u0639\u0636 \u0627\u0644\u062d\u0642\u0648\u0644 \u0627\u0644\u0642\u0627\u0628\u0644\u0629 \u0644\u0644\u062a\u0639\u062f\u064a\u0644. \u0625\u0646 \u0646\u0641\u0630\u062a \u0623\u064a \u0625\u062c\u0631\u0627\u0621 \u0641\u0633\u0648\u0641 \u062a\u062e\u0633\u0631 \u062a\u0639\u062f\u064a\u0644\u0627\u062a\u0643.",
    "abbrev. month April\u0004Apr": "\u0625\u0628\u0631\u064a\u0644",
    "abbrev. month August\u0004Aug": "\u0623\u063a\u0633\u0637\u0633",
    "abbrev. month December\u0004Dec": "\u062f\u064a\u0633\u0645\u0628\u0631",
    "abbrev. month February\u0004Feb": "\u0641\u0628\u0631\u0627\u064a\u0631",
    "abbrev. month January\u0004Jan": "\u064a\u0646\u0627\u064a\u0631",
    "abbrev. month July\u0004Jul": "\u064a\u0648\u0644\u064a\u0648",
    "abbrev. month June\u0004Jun": "\u064a\u0648\u0646\u064a\u0648",
    "abbrev. month March\u0004Mar": "\u0645\u0627\u0631\u0633",
    "abbrev. month May\u0004May": "\u0645\u0627\u064a\u0648",
    "abbrev. month November\u0004Nov": "\u0646\u0648\u0641\u0645\u0628\u0631",
    "abbrev. month October\u0004Oct": "\u0623\u0643\u062a\u0648\u0628\u0631",
    "abbrev. month September\u0004Sep": "\u0633\u0628\u062a\u0645\u0628\u0631",
    "adjudicators with gender data": "\u0627\u0644\u062d\u0643\u0627\u0645 \u0645\u0639 \u0628\u064a\u0627\u0646\u0627\u062a \u062c\u0646\u0633\u0647\u0645",
    "deselect all": "\u0625\u0644\u063a\u0627\u0621 \u062a\u062d\u062f\u064a\u062f \u0627\u0644\u0643\u0644",
    "feedback scores total": "\u0645\u062c\u0645\u0648\u0639 \u062f\u0631\u062c\u0627\u062a \u0627\u0644\u062a\u063a\u0630\u064a\u0629 \u0627\u0644\u0631\u0627\u062c\u0639\u0629 ",
    "one letter Friday\u0004F": "\u062c\u0645\u0639\u0629",
    "one letter Monday\u0004M": "\u0625\u062b\u0646\u064a\u0646",
    "one letter Saturday\u0004S": "\u0633\u0628\u062a",
    "one letter Sunday\u0004S": "\u0623\u062d\u062f",
    "one letter Thursday\u0004T": "\u062e\u0645\u064a\u0633",
    "one letter Tuesday\u0004T": "\u062b\u0644\u0627\u062b\u0627\u0621",
    "one letter Wednesday\u0004W": "\u0623\u0631\u0628\u0639\u0627\u0621",
    "select all": "\u062a\u062d\u062f\u064a\u062f \u0627\u0644\u0643\u0644",
    "speaker scores total": "\u0645\u062c\u0645\u0648\u0639 \u062f\u0631\u062c\u0627\u062a \u0627\u0644\u0645\u062a\u062d\u062f\u062b ",
    "speakers with gender data": "\u0627\u0644\u0645\u062a\u062d\u062f\u062b\u0648\u0646 \u0645\u0639 \u0628\u064a\u0627\u0646\u0627\u062a \u062c\u0646\u0633\u0647\u0645"
  };
  for (const key in newcatalog) {
    django.catalog[key] = newcatalog[key];
  }
  

  if (!django.jsi18n_initialized) {
    django.gettext = function(msgid) {
      const value = django.catalog[msgid];
      if (typeof value === 'undefined') {
        return msgid;
      } else {
        return (typeof value === 'string') ? value : value[0];
      }
    };

    django.ngettext = function(singular, plural, count) {
      const value = django.catalog[singular];
      if (typeof value === 'undefined') {
        return (count == 1) ? singular : plural;
      } else {
        return value.constructor === Array ? value[django.pluralidx(count)] : value;
      }
    };

    django.gettext_noop = function(msgid) { return msgid; };

    django.pgettext = function(context, msgid) {
      let value = django.gettext(context + '\x04' + msgid);
      if (value.includes('\x04')) {
        value = msgid;
      }
      return value;
    };

    django.npgettext = function(context, singular, plural, count) {
      let value = django.ngettext(context + '\x04' + singular, context + '\x04' + plural, count);
      if (value.includes('\x04')) {
        value = django.ngettext(singular, plural, count);
      }
      return value;
    };

    django.interpolate = function(fmt, obj, named) {
      if (named) {
        return fmt.replace(/%\(\w+\)s/g, function(match){return String(obj[match.slice(2,-2)])});
      } else {
        return fmt.replace(/%s/g, function(match){return String(obj.shift())});
      }
    };


    /* formatting library */

    django.formats = {
    "DATETIME_FORMAT": "N j, Y, P",
    "DATETIME_INPUT_FORMATS": [
      "%Y-%m-%d %H:%M:%S",
      "%Y-%m-%d %H:%M:%S.%f",
      "%Y-%m-%d %H:%M",
      "%m/%d/%Y %H:%M:%S",
      "%m/%d/%Y %H:%M:%S.%f",
      "%m/%d/%Y %H:%M",
      "%m/%d/%y %H:%M:%S",
      "%m/%d/%y %H:%M:%S.%f",
      "%m/%d/%y %H:%M"
    ],
    "DATE_FORMAT": "j F\u060c Y",
    "DATE_INPUT_FORMATS": [
      "%Y-%m-%d",
      "%m/%d/%Y",
      "%m/%d/%y",
      "%b %d %Y",
      "%b %d, %Y",
      "%d %b %Y",
      "%d %b, %Y",
      "%B %d %Y",
      "%B %d, %Y",
      "%d %B %Y",
      "%d %B, %Y"
    ],
    "DECIMAL_SEPARATOR": ",",
    "FIRST_DAY_OF_WEEK": 0,
    "MONTH_DAY_FORMAT": "j F",
    "NUMBER_GROUPING": 0,
    "SHORT_DATETIME_FORMAT": "m/d/Y P",
    "SHORT_DATE_FORMAT": "d\u200f/m\u200f/Y",
    "THOUSAND_SEPARATOR": ".",
    "TIME_FORMAT": "g:i A",
    "TIME_INPUT_FORMATS": [
      "%H:%M:%S",
      "%H:%M:%S.%f",
      "%H:%M"
    ],
    "YEAR_MONTH_FORMAT": "F Y"
  };

    django.get_format = function(format_type) {
      const value = django.formats[format_type];
      if (typeof value === 'undefined') {
        return format_type;
      } else {
        return value;
      }
    };

    /* add to global namespace */
    globals.pluralidx = django.pluralidx;
    globals.gettext = django.gettext;
    globals.ngettext = django.ngettext;
    globals.gettext_noop = django.gettext_noop;
    globals.pgettext = django.pgettext;
    globals.npgettext = django.npgettext;
    globals.interpolate = django.interpolate;
    globals.get_format = django.get_format;

    django.jsi18n_initialized = true;
  }
};

