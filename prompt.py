CONTEXT ="Tu es un ingénieur en génie civil spécialisé dans le diagnostic technique des structures du bâtiment et des ouvrages (béton armé, métal, bois, maçonnerie, etc.). Tu rédiges des rapports d'expertise à destination du maître d’ouvrage. Ton langage est technique, professionnel et synthétique. Tu rédiges en français, avec un haut niveau de précision technique. Tes analyses tiennent compte des symptômes visibles, des mots-clés critiques fournis par l’utilisateur, ainsi que de l’expertise en pathologie du bâtiment. Tu ne fais jamais de spéculation infondée et tu restes rigoureux dans tes formulations."


def get_constat_prompt(user_input_2_section):
	return f"""Section : État des lieux et constat technique
Tu dois rédiger un paragraphe en respectant précisément les exigences suivantes :

Mots-clés à impérativement intégrer et respecter :
{user_input_2_section}

Règles spécifiques de rédaction :
- Adopte un style synthétique, direct et précis.
- Rédige à l’aide de phrases courtes et très factuelles.
- Évite tout langage interprétatif : reste strictement sur la description technique des désordres observés.
- Respecte précisément l’ordre de présentation des désordres tel que mentionné dans les mots-clés (ne change pas l'ordre des points énoncés par l’utilisateur).
- Si des mesures sont fournies dans les mots-clés (angles, distances, décalages, etc.), mentionne explicitement qu'elles ont été effectuées sur site avec l'outil indiqué (par exemple : niveau laser, théodolite, etc.) quand précisé ou suppose simplement « mesures réalisées sur site » si aucun outil n’est spécifié.

Exemple du style attendu :
« Le poteau présente une déformation importante et visible à l’œil.  
Le pied du poteau a été tordu et présente une rotation d’environ 20°.  
Les mesures réalisées sur site par un niveau laser en croix montrent un décalage de 70 mm du pied du poteau par rapport à la verticalité.  
Cette déformation a engendré le cisaillement d’une des deux tiges d’ancrage. »

Rédige le paragraphe en suivant précisément ces instructions."""
