# License: GNU General Public License v3.0
#
# This file is part of ComfyUI-RvTools-X and is licensed under the GNU General Public License v3.0.
# See LICENSE file or <https://www.gnu.org/licenses/> for details.

import re
from ..core import CATEGORY

class RvText_ReplaceStringV2:
    CATEGORY = CATEGORY.MAIN.value + CATEGORY.TEXT.value
    RETURN_TYPES = ("STRING",)
    FUNCTION = "execute"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "String": ("STRING", {"default": "", "tooltip": "Input string to process."}),
                "Regex": ("STRING", {"default": "", "tooltip": "Regular expression pattern to match."}),
                "ReplaceWith": ("STRING", {"default": "", "tooltip": "Replacement string for matches."}),
                "Remove_Instructions": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "When enabled, extract content from quotes at the start of the string, or if no quotes, remove everything before the first colon (:) including the colon itself."}),                                
                "Auto_SelectFirst": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "If enabled, extract the first numbered quoted choice (1.) from LLM output and use it as the result."}),
                "List_ToPrompt_RemoveLabels": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "If enabled, convert a numbered tips list into a single-line prompt and remove short labels (e.g., 'Lighting:')."}),
                "RemDesc_Background": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "Whether to remove background description matches."}),
                "RemDesc_Subject": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "Whether to remove subject description matches."}),
                "RemDesc_Subject_Aggressive": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "When enabled, remove pronoun-led subject clauses and possessive subject phrases (aggressive)."}),
                "RemDesc_Mood": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "Whether to remove mood description matches."}),
                "RemDesc_Image": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "Whether to remove image description matches."}),
                "CleanUp": ("BOOLEAN", {"default": False, "forceInput": False, "tooltip": "When enabled, trim whitespace and remove surrounding quotes from the final output."}),
                
            }
        }

    def execute(
        self,
        String: str,
        Regex: str,
        ReplaceWith: str,
        RemDesc_Background: bool = False,
        RemDesc_Subject: bool = False,
    RemDesc_Subject_Aggressive: bool = False,
        RemDesc_Mood: bool = False,
        RemDesc_Image: bool = False,
        CleanUp: bool = False,
        Auto_SelectFirst: bool = False,
        List_ToPrompt_RemoveLabels: bool = False,
        Remove_Instructions: bool = False,
    ) -> tuple[str]:

        # Replace substrings in String using Regex and the provided replacement.
        # Additionally, when enabled and the input is not empty, remove descriptive
        # fragments for background, subject, mood, and image using targeted
        # case-insensitive regular expressions. Finally, collapse line breaks
        # into single spaces for prompt compatibility.

        s = String or ""

        # If nothing is requested (no toggles) and no regex/replace provided,
        # return the original input unchanged to avoid accidental modification.
        try:
            no_toggles = not any([
                Auto_SelectFirst,
                List_ToPrompt_RemoveLabels,
                RemDesc_Background,
                RemDesc_Subject,
                RemDesc_Subject_Aggressive,
                RemDesc_Mood,
                RemDesc_Image,
                Remove_Instructions,
            ])
        except Exception:
            no_toggles = True

        # 3) Remove instructions: extract content from inside quotes and remove everything else
        # Content extraction and processing (in logical order)
        try:
            # 1) Remove instructions first (extract core content from various formats)
            if Remove_Instructions and s.strip():
                # First try to extract content from quotes at the beginning of the string
                quote_match = re.match(r'^\s*["\']([^"\']*)["\']', s.strip())
                if quote_match:
                    s = quote_match.group(1)
                else:
                    # If no quotes at start, look for the first colon and take everything after it
                    colon_index = s.find(':')
                    if colon_index != -1:
                        s = s[colon_index + 1:].strip()

            # 2) Auto select first quoted choice (if still in choice format after extraction)
            if Auto_SelectFirst and s.strip():
                m = re.search(r'(?s)^\s*1\.\s*(?:["\'])(.*?)(?:["\'])', s, flags=re.M)
                if m:
                    s = m.group(1)

            # 3) Convert numbered lists to prompts (if still in list format)
            if List_ToPrompt_RemoveLabels and s.strip():
                # Step A: remove header up to first numbered item
                s = re.sub(r'(?s)^.*?(?=\d+\.)', '', s)
                # Step B: remove bold markup **Heading** -> Heading
                s = re.sub(r'\*\*(.*?)\*\*', r'\1', s)
                # Step C: mark numbered items with a delimiter
                s = re.sub(r'(?m)^\s*\d+\.\s*', '||', s)
                # Step D: remove short label tokens (lighting:, composition:, etc.)
                s = re.sub(r'(?i)\b(?:lighting|composition|details|background|pose|makeup|props|editing|focus|storytelling)\s*:\s*', '', s)
                # Step E: collapse newlines/tabs
                s = re.sub(r'[\r\n\t]+', ' ', s)
                # Step F: replace delimiters with comma and clean leading comma
                s = s.replace('||', ', ')
                s = re.sub(r'^,\s+', '', s)
                # Final collapse of extra spaces
                s = re.sub(r'[ ]{2,}', ' ', s).strip()
        except Exception:
            # Fail-safe: keep s unchanged on any error
            pass


        # Only operate if there is input text
        if s.strip():
            # Patterns are intentionally conservative: they remove labelled or
            # short descriptive clauses commonly used in prompts, such as
            # "background: ...", "subject: ...", "mood: ...", or
            # parenthetical/image-type descriptors. Flags: DOTALL + IGNORECASE.
            try:
                # Background descriptors: labels and short phrases; also match
                # short sentences that start after punctuation and optional 'The',
                # e.g. ". The background is a plain grey color." Keep conservative.
                background_pat = r"(?i)(?:(?:backgrounds?|environment|setting|scene|surroundings)\s*[:\-–]?\s*[^\n\.;]+[\n\.;]?|(?:[\.\?!]\s*(?:The\s+)?(?:backgrounds?|environment|setting|scene|surroundings)\s+[^\n\.;]+[\n\.;]?))"
                # Subject descriptors: labels like 'subject:', or mentions at line start
                subject_pat = r"(?i)(?:subject|person|people|man|woman|girl|boy|character)\s*[:\-–]?\s*[^\n\.;]+[\n\.;]?"
                # Mood descriptors: mood/atmosphere/vibe descriptors. Also match
                # variants like ". The mood is ..." and "The overall mood of the image is ...".
                # Match at start-of-string or after sentence terminator so leading
                # words like "The overall" are removed together with the mood clause.
                mood_pat = r"(?is)(?:\b(?:mood|moods|feeling|feelings|atmosphere|vibe|vibes)\b\s*[:\-–]?\s*[^\n\.;]+[\n\.;]?|(?:^|[\.\?!]\s*)(?:The\s+)?(?:overall\s+)?(?:mood|moods|feeling|feelings|atmosphere|vibe|vibes)(?:\s+of(?:\s+the)?\s+(?:image|photograph|photo|scene|shot))?(?:\s+is|\s+are)?\s+[^\n\.;]+[\n\.;]?)"
                # Image descriptors: conservative matching only for explicit
                # image/photo labels or "The image is ..." phrasing, BUT
                # avoid removing fragments that describe the subject (portrait,
                # woman, man, person, etc.). We use a negative lookahead to
                # skip matches containing those subject tokens.
                image_pat = r"(?i)(?:(?:\b(?:image|photo|photograph|picture|shot|render|illustration)\b)\s*(?:[:\-–]\s*|(?:is|was)\s+)(?![^\n\.;]{0,120}\b(?:portrait|woman|man|girl|boy|person|people|subject)\b)[^\n\.;]{1,200}[\n\.;]?)"

                # Helper: if the matched fragment starts with a sentence terminator
                # (., ?, !) preserve that terminator and a following space so
                # sentences don't run together when a fragment is removed.
                def _preserve_lead(match):
                    lead = re.match(r'^\s*([\.\?!])\s*', match.group(0))
                    if lead:
                        return lead.group(1) + ' '
                    return ''

                if RemDesc_Background:
                    s = re.sub(background_pat, _preserve_lead, s, flags=re.S)
                if RemDesc_Subject:
                    # Remove subject-style sentences that start at the beginning
                    # of the string or immediately after a sentence terminator.
                    # Also allow an optional leading 'The ' and preserve any
                    # leading terminator via the backreference so sentences
                    # don't run together.
                    # Include pronouns and age descriptors to catch subject sentences
                    subj_inner = r"(?:(?:subject|person|people|man|woman|girl|boy|character)|(?:he|she|him|her|they|them)|(?:young|old|elderly|teenage|middle-?aged|child|baby|adult))\b\s*[^\n\.;]*[\n\.;]?"
                    s = re.sub(r'(^|[\.\?!]\s)(?:The\s+)?' + subj_inner, r"\1", s, flags=re.S|re.I)
                    # Also remove labeled inline subject tokens (e.g., 'subject: ...')
                    s = re.sub(subject_pat, "", s, flags=re.S)
                if RemDesc_Mood:
                    s = re.sub(mood_pat, _preserve_lead, s, flags=re.S)
                if RemDesc_Image:
                    # Targeted removal for common leading image descriptors that
                    # should be stripped (we want to keep the subject phrase):
                    # - "The image is"                  -> remove
                    # - "close-up portrait of" / "portrait of" -> remove the prefix
                    # - "headshot of"                   -> remove the prefix
                    # Apply these conservatively only at sentence starts.
                    s = re.sub(r'(?i)^[\s]*the\s+image\s+is\s+', '', s)
                    s = re.sub(r'(?i)^(?:.*?\b)?(?:close[- ]?up\s+portrait\s+of\s+|portrait\s+of\s+|headshot\s+of\s+)', '', s)
                    # Remove illustration/painting/drawing/photograph prefixes at starts of sentences
                    s = re.sub(r'(?i)^[\s]*(?:a|an)\s+(?:digital\s+)?(?:illustration|painting|drawing|sketch|photograph|photo)\s+of\s+', '', s)
                    # Only remove explicit image/photo fragments when they
                    # appear at the start of the string or immediately after
                    # a sentence terminator + space. Preserve the terminator.
                    image_inner = (
                        r"(?:\b(?:image|photo|photograph|picture|shot|render|illustration)\b)"
                        r"\s*(?:[:\-–]\s*|(?:is|was)\s+)"
                        r"(?![^\n\.;]{0,120}\b(?:portrait|woman|man|girl|boy|person|people|subject)\b)"
                        r"[^\n\.;]{1,200}[\n\.;]?"
                    )
                    # Match either at start (^) or after a sentence terminator + space
                    s = re.sub(r'(^|[\.\?!]\s)'+image_inner, r'\1', s, flags=re.S|re.I)
                # Aggressive subject removals: optional, enabled by toggle.
                if RemDesc_Subject_Aggressive:
                    # 0) Strip leading pronoun + copula while preserving the verb phrase.
                    #    "She is looking directly" -> "looking directly"
                    try:
                        pronoun_copula = re.compile(r'(?i)(^|[\.\?!]\s+)(?:The\s+)?\b(?:she|he|they|her|him|them|his|our|my)\b\s+(?:is|are|was|were|seems|appear(?:s)?|looks?)\s+', flags=re.S)
                        def _strip_pronoun_copula(m):
                            return m.group(1) or ''
                        s = pronoun_copula.sub(_strip_pronoun_copula, s)
                    except Exception:
                        pass

                    # 1) Anchored pronoun sentences (preserve leading terminator)
                    pronoun_sentence_anchor = r'(^|[\.\?!]\s+)(?:The\s+)?(?:she|he|they|her|his|them|him)\b[^\n\.;]{0,200}[\n\.;]?'
                    s = re.sub(pronoun_sentence_anchor, _preserve_lead, s, flags=re.I|re.S)
                    # 2) Remove possessive subject phrases (her face, his hands, their eyes)
                    possessive_phrases = r"\b(?:her|his|their|my|our)\s+(?:face|eyes|hands|hair|skin|expression|eyebrows|mouth|nose|chin|cheeks|lips|teeth)\b[\w\s,\-]{0,80}"
                    s = re.sub(possessive_phrases, '', s, flags=re.I)
                    # 3) Fallback: remove any remaining short pronoun-led clause fragments
                    pronoun_sentence_any = r'(?<!\w)(?:she|he|they|her|him|them|his)\b[^\n\.;]{0,200}[\n\.;]?'
                    s = re.sub(pronoun_sentence_any, '', s, flags=re.I|re.S)
            except Exception:
                # If any pattern fails, fall back to original string silently
                pass

        # Apply the user-provided regex replacement (keep original behavior)
        try:
            if Regex and str(Regex).strip():
                # If Regex is provided, run replacement. ReplaceWith may be empty
                # which effectively removes matches.
                replaced = re.sub(Regex, ReplaceWith, s)
            else:
                # No user regex -> keep the string as-is (after description removals)
                replaced = s
        except Exception:
            # If the user regex is invalid, avoid crashing and return original + normalized spaces
            replaced = s

        # Optionally cleanup: comprehensive text normalization and quote removal
        if CleanUp:
            # Normalize whitespace and newlines for prompt safety
            replaced = re.sub(r"[\r\n]+", " ", replaced)
            # Collapse multiple spaces to single space
            replaced = re.sub(r"[ ]{2,}", " ", replaced)
            # Small cosmetic cleanup: when aggressive removals leave a dangling
            # period followed by a space before a lowercase-word (e.g., "a young . looking"),
            # remove the dot and the extra space so the phrase becomes "a young looking".
            # We make this conservative: only remove a single '.' followed by space and a
            # lowercase letter (common after our pronoun/copula strip).
            try:
                replaced = re.sub(r'\s*\.\s+(?=[a-z])', ' ', replaced)
            except Exception:
                pass
            replaced = replaced.strip()
            # remove double quote characters (preserve single quotes for apostrophes)
            replaced = replaced.replace('"', '')
            # replace ". ," with ". " (including any whitespace after comma)
            replaced = re.sub(r'\. ,\s*', '. ', replaced)
        else:
            replaced = replaced
        return (replaced,)

NODE_NAME = 'Replace String v2 [RvTools-X]'
NODE_DESC = 'Replace String v2'

NODE_CLASS_MAPPINGS = {
    NODE_NAME: RvText_ReplaceStringV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    NODE_NAME: NODE_DESC
}