package com.eerussianguy.firmalife.client.render;

import java.util.function.Function;

import net.minecraft.client.Minecraft;
import net.minecraft.client.renderer.MultiBufferSource;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.blockentity.BlockEntityRenderer;
import net.minecraft.client.renderer.texture.TextureAtlasSprite;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.inventory.InventoryMenu;

import com.eerussianguy.firmalife.common.blockentities.HangingPlanterBlockEntity;
import com.eerussianguy.firmalife.common.util.Plantable;
import com.mojang.blaze3d.vertex.PoseStack;
import com.mojang.blaze3d.vertex.VertexConsumer;
import net.dries007.tfc.client.RenderHelpers;

public class HangingPlanterBlockEntityRenderer implements BlockEntityRenderer<HangingPlanterBlockEntity>
{
    private static final int FRUIT_ID = 0;

    @Override
    public void render(HangingPlanterBlockEntity planter, float partialTicks, PoseStack poseStack, MultiBufferSource buffers, int combinedLight, int combinedOverlay)
    {
        final Plantable plant = planter.getPlantable(0);
        if (plant == null) return;

        poseStack.pushPose();
        final Function<ResourceLocation, TextureAtlasSprite> atlas = Minecraft.getInstance().getTextureAtlas(InventoryMenu.BLOCK_ATLAS);
        final TextureAtlasSprite growth = atlas.apply(plant.getTexture(planter.getGrowth(0)));
        final VertexConsumer buffer = buffers.getBuffer(RenderType.cutout());

        // foliage
        RenderUtils.renderCross(1 / 16f, 15 / 16f, 0 / 16f, 13 / 16f, poseStack, buffer, combinedLight, combinedOverlay, growth, 1f / 16f, 0f, 15f / 16f, 13f / 16f);

        // fruits
        if (planter.getGrowth(0) >= 1f)
        {
            TextureAtlasSprite fruit = atlas.apply(plant.getSpecialTexture(FRUIT_ID));
            RenderHelpers.renderTexturedCuboid(poseStack, buffer, fruit, combinedLight, combinedOverlay, 4 / 16f, 3 / 16f, 4 / 16f, 7 / 16f, 6 / 16f, 7 / 16f);
            RenderHelpers.renderTexturedCuboid(poseStack, buffer, fruit, combinedLight, combinedOverlay, 4 / 16f, (float) 0, 10 / 16f, 7 / 16f, 3 / 16f, 13 / 16f);
            RenderHelpers.renderTexturedCuboid(poseStack, buffer, fruit, combinedLight, combinedOverlay, 9 / 16f, 7 / 16f, 5 / 16f, 12 / 16f, 10 / 16f, 8 / 16f);
        }

        poseStack.popPose();
    }
}
